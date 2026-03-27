"""
D&D Law Associates — Manupatra Judgment Cache
SQLite database with FTS5 full-text search for caching judgments
extracted from Manupatra via Chrome browser automation.

Follows the same pattern as database.py (WAL mode, FTS5, triggers).
Separate database (manupatra_cache.db) to keep judgment data
independent from the chamber drafts library.
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta

from .config import CACHE_DB_PATH, CACHE_MAX_AGE_DAYS


def get_connection(db_path=None):
    """Get a database connection with WAL mode for performance."""
    if db_path is None:
        db_path = CACHE_DB_PATH
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def initialize_database(conn=None):
    """Create tables, FTS5 virtual table, and sync triggers."""
    close_after = False
    if conn is None:
        conn = get_connection()
        close_after = True

    conn.executescript("""
        -- ══════════════════════════════════════════
        -- Main judgments table
        -- ══════════════════════════════════════════
        CREATE TABLE IF NOT EXISTS judgments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citation TEXT NOT NULL UNIQUE,
            manu_id TEXT,
            court TEXT NOT NULL,
            court_code TEXT,
            bench TEXT,
            date_decided TEXT,
            year INTEGER,
            parties TEXT NOT NULL,
            appellant TEXT,
            respondent TEXT,
            subject TEXT,
            headnotes TEXT,
            full_text TEXT,
            statutes_referred TEXT,
            cases_referred TEXT,
            source_url TEXT,
            cached_at TEXT NOT NULL DEFAULT (datetime('now')),
            text_length INTEGER DEFAULT 0,
            search_context TEXT
        );

        -- ══════════════════════════════════════════
        -- FTS5 index for offline full-text search
        -- ══════════════════════════════════════════
        CREATE VIRTUAL TABLE IF NOT EXISTS judgments_fts USING fts5(
            citation,
            parties,
            headnotes,
            full_text,
            statutes_referred,
            court,
            bench,
            content=judgments,
            content_rowid=id
        );

        -- ══════════════════════════════════════════
        -- Sync triggers: keep FTS5 in sync with judgments table
        -- ══════════════════════════════════════════
        CREATE TRIGGER IF NOT EXISTS judgments_ai AFTER INSERT ON judgments BEGIN
            INSERT INTO judgments_fts(rowid, citation, parties, headnotes, full_text, statutes_referred, court, bench)
            VALUES (new.id, new.citation, new.parties, new.headnotes, new.full_text, new.statutes_referred, new.court, new.bench);
        END;

        CREATE TRIGGER IF NOT EXISTS judgments_ad AFTER DELETE ON judgments BEGIN
            INSERT INTO judgments_fts(judgments_fts, rowid, citation, parties, headnotes, full_text, statutes_referred, court, bench)
            VALUES ('delete', old.id, old.citation, old.parties, old.headnotes, old.full_text, old.statutes_referred, old.court, old.bench);
        END;

        CREATE TRIGGER IF NOT EXISTS judgments_au AFTER UPDATE ON judgments BEGIN
            INSERT INTO judgments_fts(judgments_fts, rowid, citation, parties, headnotes, full_text, statutes_referred, court, bench)
            VALUES ('delete', old.id, old.citation, old.parties, old.headnotes, old.full_text, old.statutes_referred, old.court, old.bench);
            INSERT INTO judgments_fts(rowid, citation, parties, headnotes, full_text, statutes_referred, court, bench)
            VALUES (new.id, new.citation, new.parties, new.headnotes, new.full_text, new.statutes_referred, new.court, new.bench);
        END;

        -- ══════════════════════════════════════════
        -- Search history table
        -- ══════════════════════════════════════════
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            court_filter TEXT,
            date_filter TEXT,
            results_count INTEGER DEFAULT 0,
            cached_count INTEGER DEFAULT 0,
            searched_at TEXT NOT NULL DEFAULT (datetime('now'))
        );

        -- ══════════════════════════════════════════
        -- Indexes for common queries
        -- ══════════════════════════════════════════
        CREATE INDEX IF NOT EXISTS idx_judgments_court ON judgments(court);
        CREATE INDEX IF NOT EXISTS idx_judgments_year ON judgments(year);
        CREATE INDEX IF NOT EXISTS idx_judgments_date ON judgments(date_decided);
        CREATE INDEX IF NOT EXISTS idx_judgments_manu ON judgments(manu_id);
        CREATE INDEX IF NOT EXISTS idx_judgments_cached ON judgments(cached_at);
    """)

    conn.commit()
    if close_after:
        conn.close()


def cache_judgment(
    citation: str,
    court: str,
    parties: str,
    date_decided: str = "",
    bench: str = "",
    headnotes: str = "",
    full_text: str = "",
    source_url: str = "",
    manu_id: str = "",
    court_code: str = "",
    appellant: str = "",
    respondent: str = "",
    subject: str = "",
    statutes_referred: str = "",
    cases_referred: str = "",
    search_context: str = "",
):
    """
    Cache a judgment in the local SQLite database.
    Uses INSERT OR REPLACE — if citation already exists, updates it.

    Args:
        citation: Case citation (e.g., "(2023) 5 SCC 123")
        court: Court name (e.g., "Supreme Court")
        parties: Case title (e.g., "Ram vs Shyam")
        date_decided: Date in DD-MM-YYYY or YYYY-MM-DD format
        bench: Bench composition
        headnotes: Headnote or ratio text
        full_text: Full judgment text
        source_url: Manupatra URL
        manu_id: MANU citation ID (e.g., "MANU/SC/0123/2023")
        court_code: Court abbreviation (e.g., "SC")
        appellant: Appellant name
        respondent: Respondent name
        subject: Subject area (e.g., "Civil", "Criminal")
        statutes_referred: Comma-separated statutes
        cases_referred: Comma-separated cited cases
        search_context: What search led to finding this case

    Returns:
        dict with id, citation, and status
    """
    conn = get_connection()
    initialize_database(conn)

    # Extract year from date or citation
    year = None
    if date_decided:
        try:
            parts = date_decided.split("-")
            if len(parts[0]) == 4:  # YYYY-MM-DD
                year = int(parts[0])
            elif len(parts[2]) == 4:  # DD-MM-YYYY
                year = int(parts[2])
        except (ValueError, IndexError):
            pass
    if not year:
        import re
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', citation)
        if year_match:
            year = int(year_match.group(1))

    # Extract appellant/respondent from parties if not provided
    if parties and not appellant:
        vs_parts = parties.split(" vs ", 1) if " vs " in parties.lower() else parties.split(" v. ", 1) if " v. " in parties.lower() else [parties]
        if len(vs_parts) == 2:
            appellant = vs_parts[0].strip()
            respondent = vs_parts[1].strip()

    text_length = len(full_text) if full_text else 0

    try:
        conn.execute("""
            INSERT OR REPLACE INTO judgments
            (citation, manu_id, court, court_code, bench, date_decided, year,
             parties, appellant, respondent, subject, headnotes, full_text,
             statutes_referred, cases_referred, source_url, text_length,
             search_context, cached_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (
            citation, manu_id, court, court_code, bench, date_decided, year,
            parties, appellant, respondent, subject, headnotes, full_text,
            statutes_referred, cases_referred, source_url, text_length,
            search_context
        ))
        conn.commit()
        row_id = conn.execute(
            "SELECT id FROM judgments WHERE citation = ?", (citation,)
        ).fetchone()
        conn.close()
        return {
            "id": row_id["id"] if row_id else None,
            "citation": citation,
            "status": "cached",
            "text_length": text_length,
        }
    except sqlite3.Error as e:
        conn.close()
        return {"citation": citation, "status": "error", "error": str(e)}


def get_judgment(citation: str):
    """
    Get a specific cached judgment by citation or MANU ID.
    Tries exact match first, then partial match.
    """
    conn = get_connection()
    initialize_database(conn)

    # Try exact citation match
    row = conn.execute(
        "SELECT * FROM judgments WHERE citation = ?", (citation,)
    ).fetchone()

    # Try MANU ID match
    if not row and citation.startswith("MANU/"):
        row = conn.execute(
            "SELECT * FROM judgments WHERE manu_id = ?", (citation,)
        ).fetchone()

    # Try partial match (case-insensitive)
    if not row:
        row = conn.execute(
            "SELECT * FROM judgments WHERE citation LIKE ? OR manu_id LIKE ?",
            (f"%{citation}%", f"%{citation}%")
        ).fetchone()

    conn.close()
    return dict(row) if row else None


def search_cached(query: str, court: str = "", year: str = "", limit: int = 15):
    """
    Search locally cached judgments using FTS5 full-text search.
    Falls back to LIKE search if FTS5 returns no results.

    Args:
        query: Search keywords
        court: Optional court filter
        year: Optional year filter (single year or range "2020-2024")
        limit: Maximum results (default 15)

    Returns:
        List of judgment dicts (without full_text to keep response small)
    """
    conn = get_connection()
    initialize_database(conn)

    # Try FTS5 search first
    fts_query = " OR ".join(f'"{term}"*' for term in query.split())
    sql = """
        SELECT j.id, j.citation, j.manu_id, j.court, j.court_code, j.bench,
               j.date_decided, j.year, j.parties, j.appellant, j.respondent,
               j.subject, j.headnotes, j.statutes_referred, j.cases_referred,
               j.source_url, j.text_length, j.cached_at, j.search_context,
               rank
        FROM judgments_fts fts
        JOIN judgments j ON j.id = fts.rowid
        WHERE judgments_fts MATCH ?
    """
    params = [fts_query]

    if court:
        sql += " AND j.court LIKE ?"
        params.append(f"%{court}%")
    if year:
        if "-" in year:
            y1, y2 = year.split("-", 1)
            sql += " AND j.year BETWEEN ? AND ?"
            params.extend([int(y1), int(y2)])
        else:
            sql += " AND j.year = ?"
            params.append(int(year))

    sql += " ORDER BY rank LIMIT ?"
    params.append(limit)

    try:
        results = conn.execute(sql, params).fetchall()
        if results:
            conn.close()
            return [dict(r) for r in results]
    except sqlite3.OperationalError:
        pass

    # Fallback to LIKE search
    sql = """
        SELECT id, citation, manu_id, court, court_code, bench,
               date_decided, year, parties, appellant, respondent,
               subject, headnotes, statutes_referred, cases_referred,
               source_url, text_length, cached_at, search_context
        FROM judgments
        WHERE (citation LIKE ? OR parties LIKE ? OR headnotes LIKE ?
               OR statutes_referred LIKE ? OR court LIKE ?)
    """
    pattern = f"%{query}%"
    params = [pattern, pattern, pattern, pattern, pattern]

    if court:
        sql += " AND court LIKE ?"
        params.append(f"%{court}%")
    if year:
        if "-" in year:
            y1, y2 = year.split("-", 1)
            sql += " AND year BETWEEN ? AND ?"
            params.extend([int(y1), int(y2)])
        else:
            sql += " AND year = ?"
            params.append(int(year))

    sql += " ORDER BY year DESC, date_decided DESC LIMIT ?"
    params.append(limit)

    results = conn.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in results]


def get_cache_stats():
    """Get statistics on cached judgments."""
    conn = get_connection()
    initialize_database(conn)

    stats = {
        "total_judgments": 0,
        "by_court": {},
        "by_year": {},
        "total_text_chars": 0,
        "db_size_kb": 0,
        "recent_searches": [],
        "oldest_cache": None,
        "newest_cache": None,
    }

    try:
        stats["total_judgments"] = conn.execute(
            "SELECT COUNT(*) FROM judgments"
        ).fetchone()[0]

        for row in conn.execute(
            "SELECT court, COUNT(*) as cnt FROM judgments GROUP BY court ORDER BY cnt DESC"
        ):
            stats["by_court"][row["court"]] = row["cnt"]

        for row in conn.execute(
            "SELECT year, COUNT(*) as cnt FROM judgments WHERE year IS NOT NULL GROUP BY year ORDER BY year DESC"
        ):
            stats["by_year"][str(row["year"])] = row["cnt"]

        total_chars = conn.execute(
            "SELECT COALESCE(SUM(text_length), 0) FROM judgments"
        ).fetchone()[0]
        stats["total_text_chars"] = total_chars

        if os.path.exists(CACHE_DB_PATH):
            stats["db_size_kb"] = round(os.path.getsize(CACHE_DB_PATH) / 1024, 1)

        oldest = conn.execute(
            "SELECT MIN(cached_at) FROM judgments"
        ).fetchone()[0]
        newest = conn.execute(
            "SELECT MAX(cached_at) FROM judgments"
        ).fetchone()[0]
        stats["oldest_cache"] = oldest
        stats["newest_cache"] = newest

        # Recent searches
        searches = conn.execute(
            "SELECT query, court_filter, results_count, searched_at "
            "FROM search_history ORDER BY searched_at DESC LIMIT 10"
        ).fetchall()
        stats["recent_searches"] = [dict(s) for s in searches]

    except sqlite3.Error:
        pass

    conn.close()
    return stats


def list_recent(limit: int = 20):
    """List recently cached judgments."""
    conn = get_connection()
    initialize_database(conn)

    results = conn.execute("""
        SELECT id, citation, manu_id, court, date_decided, year, parties,
               text_length, cached_at, search_context
        FROM judgments
        ORDER BY cached_at DESC
        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()
    return [dict(r) for r in results]


def log_search(query: str, court_filter: str = "", date_filter: str = "",
               results_count: int = 0, cached_count: int = 0):
    """Log a search query for history tracking."""
    conn = get_connection()
    initialize_database(conn)

    conn.execute("""
        INSERT INTO search_history (query, court_filter, date_filter, results_count, cached_count)
        VALUES (?, ?, ?, ?, ?)
    """, (query, court_filter, date_filter, results_count, cached_count))

    conn.commit()
    conn.close()


def clear_expired():
    """Remove cached judgments older than CACHE_MAX_AGE_DAYS."""
    conn = get_connection()
    initialize_database(conn)

    cutoff = (datetime.now() - timedelta(days=CACHE_MAX_AGE_DAYS)).isoformat()
    deleted = conn.execute(
        "DELETE FROM judgments WHERE cached_at < ?", (cutoff,)
    ).rowcount
    conn.commit()
    conn.close()
    return deleted


def delete_judgment(citation: str):
    """Delete a specific cached judgment."""
    conn = get_connection()
    initialize_database(conn)
    deleted = conn.execute(
        "DELETE FROM judgments WHERE citation = ?", (citation,)
    ).rowcount
    conn.commit()
    conn.close()
    return deleted


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "init":
        initialize_database()
        print(f"Database initialized at: {CACHE_DB_PATH}")
    elif len(sys.argv) > 1 and sys.argv[1] == "stats":
        stats = get_cache_stats()
        print(f"Total judgments: {stats['total_judgments']}")
        print(f"DB size: {stats['db_size_kb']} KB")
        if stats['by_court']:
            print("\nBy Court:")
            for c, n in stats['by_court'].items():
                print(f"  {c}: {n}")
    elif len(sys.argv) > 2 and sys.argv[1] == "search":
        query = " ".join(sys.argv[2:])
        results = search_cached(query)
        print(f"Found {len(results)} cached results for '{query}':")
        for r in results:
            print(f"  [{r['citation']}] {r['parties']} ({r['court']}, {r['year']})")
    else:
        print("Usage:")
        print("  python3 cache.py init           # Initialize database")
        print("  python3 cache.py stats          # Cache statistics")
        print("  python3 cache.py search <query> # Search cached judgments")
