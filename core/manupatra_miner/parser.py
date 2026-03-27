"""
D&D Law Associates — Manupatra Page Text Parser
Parses raw text extracted from Manupatra pages (via Chrome MCP get_page_text)
into structured judgment data.

NOTE: These parsers use heuristic regex patterns that may need calibration
after the first live browser session against Manupatra. The patterns are
designed to be tolerant of formatting variations.
"""

import re
from .config import CITATION_PATTERNS, STATUTE_PATTERNS


def parse_search_results(page_text: str) -> list:
    """
    Parse Manupatra search results page text into structured results.

    Args:
        page_text: Raw text from get_page_text on a Manupatra search results page.

    Returns:
        List of dicts: [{title, citation, court, date, snippet, url}, ...]
    """
    results = []
    if not page_text:
        return results

    # Split into potential result blocks
    # Manupatra typically separates results with horizontal lines or numbered entries
    lines = page_text.split("\n")

    current_result = {}
    for line in lines:
        line = line.strip()
        if not line:
            if current_result and current_result.get("title"):
                results.append(current_result)
                current_result = {}
            continue

        # Try to detect citations in the line
        citation = _extract_first_citation(line)
        if citation and not current_result.get("citation"):
            current_result["citation"] = citation

        # Try to detect court name
        court = _extract_court_from_line(line)
        if court and not current_result.get("court"):
            current_result["court"] = court

        # Try to detect date
        date = _extract_date_from_line(line)
        if date and not current_result.get("date"):
            current_result["date"] = date

        # If line looks like a case title (contains "vs" or "v.")
        if _looks_like_title(line) and not current_result.get("title"):
            current_result["title"] = line

        # Accumulate snippet text
        if current_result.get("title") and len(line) > 20:
            if "snippet" not in current_result:
                current_result["snippet"] = line
            elif len(current_result["snippet"]) < 500:
                current_result["snippet"] += " " + line

    # Don't forget the last result
    if current_result and current_result.get("title"):
        results.append(current_result)

    return results


def parse_judgment_page(page_text: str) -> dict:
    """
    Parse a Manupatra judgment detail page into structured data.

    Args:
        page_text: Raw text from get_page_text on a judgment page.

    Returns:
        Dict with: citation, court, bench, date, parties, headnotes,
                    full_text, statutes_referred, cases_referred
    """
    result = {
        "citation": "",
        "manu_id": "",
        "court": "",
        "bench": "",
        "date_decided": "",
        "parties": "",
        "appellant": "",
        "respondent": "",
        "headnotes": "",
        "full_text": "",
        "statutes_referred": [],
        "cases_referred": [],
    }

    if not page_text:
        return result

    lines = page_text.split("\n")
    full_text_lines = []
    in_headnotes = False
    in_judgment = False
    headnote_lines = []

    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # ── Extract Citation ──
        if not result["citation"]:
            citation = _extract_first_citation(line_stripped)
            if citation:
                result["citation"] = citation

        # ── Extract MANU ID ──
        if not result["manu_id"]:
            manu_match = re.search(r'MANU/\w+/\d+/\d{4}', line_stripped)
            if manu_match:
                result["manu_id"] = manu_match.group()

        # ── Extract Court ──
        if not result["court"]:
            court = _extract_court_from_line(line_stripped)
            if court:
                result["court"] = court

        # ── Extract Bench / Coram ──
        if not result["bench"]:
            bench_match = re.search(
                r'(?:Bench|Coram|Before|Hon\'?ble)\s*[:\-]?\s*(.+)',
                line_stripped, re.IGNORECASE
            )
            if bench_match:
                bench_text = bench_match.group(1).strip()
                if "Justice" in bench_text or "J." in bench_text or "JJ." in bench_text:
                    result["bench"] = bench_text

        # ── Extract Date ──
        if not result["date_decided"]:
            date = _extract_date_from_line(line_stripped)
            if date:
                result["date_decided"] = date

        # ── Extract Parties ──
        if not result["parties"] and _looks_like_title(line_stripped):
            result["parties"] = line_stripped
            vs_parts = _split_parties(line_stripped)
            if vs_parts:
                result["appellant"] = vs_parts[0]
                result["respondent"] = vs_parts[1]

        # ── Detect Headnote Section ──
        if re.search(r'Head\s*[Nn]ote|HEADNOTE|HEAD NOTE', line_stripped):
            in_headnotes = True
            in_judgment = False
            continue

        # ── Detect Judgment Section ──
        if re.search(r'JUDGMENT|J\s*U\s*D\s*G\s*M\s*E\s*N\s*T|ORDER', line_stripped):
            in_headnotes = False
            in_judgment = True
            continue

        # ── Accumulate text ──
        if in_headnotes:
            headnote_lines.append(line_stripped)
        if in_judgment or (not in_headnotes and len(line_stripped) > 30):
            full_text_lines.append(line_stripped)

    # Assemble results
    result["headnotes"] = "\n".join(headnote_lines) if headnote_lines else ""
    result["full_text"] = "\n".join(full_text_lines) if full_text_lines else page_text

    # Extract statute and case references from full text
    result["statutes_referred"] = extract_statutes_referred(result["full_text"])
    result["cases_referred"] = extract_cases_referred(result["full_text"])

    return result


def extract_statutes_referred(text: str) -> list:
    """
    Extract statute/section references from judgment text.

    Returns:
        List of strings like ["Section 9 CPC", "Order 39 Rule 1 CPC", "Article 226 Constitution"]
    """
    if not text:
        return []

    refs = set()
    for pattern in STATUTE_PATTERNS:
        for match in pattern.finditer(text):
            groups = match.groups()
            if len(groups) >= 2:
                ref = f"Section {groups[0]} of {groups[1].strip()}"
            elif len(groups) == 1:
                ref = match.group().strip()
            else:
                ref = match.group().strip()
            # Clean up
            ref = re.sub(r'\s+', ' ', ref).strip()
            if len(ref) < 100:  # Skip overly long matches (false positives)
                refs.add(ref)

    return sorted(refs)


def extract_cases_referred(text: str) -> list:
    """
    Extract cited case citations from judgment text.

    Returns:
        List of citation strings found in the text.
    """
    if not text:
        return []

    cases = set()
    for pattern, _fmt in CITATION_PATTERNS:
        for match in pattern.finditer(text):
            cases.add(match.group().strip())

    return sorted(cases)


def clean_judgment_text(raw_text: str) -> str:
    """
    Clean Manupatra page text — remove navigation artifacts, headers,
    footers, watermarks, and other non-judgment content.
    """
    if not raw_text:
        return ""

    lines = raw_text.split("\n")
    cleaned = []

    skip_patterns = [
        re.compile(r'^\s*Home\s*\|', re.IGNORECASE),
        re.compile(r'^\s*Search\s+Result', re.IGNORECASE),
        re.compile(r'^\s*Print\s+Page', re.IGNORECASE),
        re.compile(r'^\s*Copyright\s+', re.IGNORECASE),
        re.compile(r'^\s*Manupatra\s', re.IGNORECASE),
        re.compile(r'^\s*www\.manupatra', re.IGNORECASE),
        re.compile(r'^\s*All\s+Rights\s+Reserved', re.IGNORECASE),
        re.compile(r'^\s*Log\s*[Oo]ut', re.IGNORECASE),
        re.compile(r'^\s*My\s+Account', re.IGNORECASE),
        re.compile(r'^\s*\d+\s*of\s*\d+\s*$'),  # Page numbers like "1 of 25"
        re.compile(r'^\s*Page\s+\d+', re.IGNORECASE),
    ]

    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned.append("")
            continue

        # Skip navigation/boilerplate lines
        if any(p.search(stripped) for p in skip_patterns):
            continue

        cleaned.append(stripped)

    # Remove excessive blank lines
    text = "\n".join(cleaned)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ═══════════════════════════════════════════════════════════════
# INTERNAL HELPERS
# ═══════════════════════════════════════════════════════════════

def _extract_first_citation(text: str) -> str:
    """Extract the first citation found in text."""
    for pattern, _fmt in CITATION_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group().strip()
    return ""


def _extract_court_from_line(line: str) -> str:
    """Extract court name from a text line."""
    court_patterns = [
        (r'Supreme\s+Court\s+of\s+India', "Supreme Court of India"),
        (r'Supreme\s+Court', "Supreme Court of India"),
        (r'High\s+Court\s+of\s+(\w[\w\s&]+)', None),  # Dynamic capture
        (r'(\w+)\s+High\s+Court', None),
        (r'National\s+Consumer\s+Disputes\s+Redressal\s+Commission', "NCDRC"),
        (r'National\s+Company\s+Law\s+Tribunal', "NCLT"),
        (r'National\s+Company\s+Law\s+Appellate\s+Tribunal', "NCLAT"),
        (r'Debt\s+Recovery\s+Tribunal', "DRT"),
        (r'Debt\s+Recovery\s+Appellate\s+Tribunal', "DRAT"),
    ]

    for pattern, static_name in court_patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            if static_name:
                return static_name
            else:
                return match.group().strip()
    return ""


def _extract_date_from_line(line: str) -> str:
    """Extract a date from a text line. Returns DD-MM-YYYY format."""
    # DD/MM/YYYY or DD-MM-YYYY or DD.MM.YYYY
    date_match = re.search(r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})', line)
    if date_match:
        d, m, y = date_match.groups()
        return f"{d.zfill(2)}-{m.zfill(2)}-{y}"

    # Month name format: 15 March 2023, March 15, 2023
    month_names = {
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }
    # "15 March 2023" or "15th March 2023"
    match = re.search(r'(\d{1,2})(?:st|nd|rd|th)?\s+(\w+)\s+(\d{4})', line)
    if match:
        d, m_name, y = match.groups()
        m = month_names.get(m_name.lower())
        if m:
            return f"{d.zfill(2)}-{m}-{y}"

    # "March 15, 2023"
    match = re.search(r'(\w+)\s+(\d{1,2}),?\s+(\d{4})', line)
    if match:
        m_name, d, y = match.groups()
        m = month_names.get(m_name.lower())
        if m:
            return f"{d.zfill(2)}-{m}-{y}"

    # "Decided on: 2023-03-15"
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', line)
    if match:
        y, m, d = match.groups()
        return f"{d}-{m}-{y}"

    return ""


def _looks_like_title(line: str) -> str:
    """Check if a line looks like a case title (contains vs/v. pattern)."""
    if len(line) < 5 or len(line) > 300:
        return False
    return bool(re.search(r'\b(?:vs\.?|v\.)\b', line, re.IGNORECASE))


def _split_parties(title: str) -> tuple:
    """Split a case title into (appellant, respondent)."""
    for sep in [" vs. ", " vs ", " Vs. ", " Vs ", " VS ", " v. ", " V. "]:
        if sep in title:
            parts = title.split(sep, 1)
            return (parts[0].strip(), parts[1].strip())
    return None
