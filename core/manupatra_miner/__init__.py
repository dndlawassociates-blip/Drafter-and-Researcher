"""
D&D Law Associates — Manupatra Case Law Mining Module
Searches, caches, and formats Indian case law from Manupatra.

Architecture:
  Python Layer (this module): URL construction, SQLite caching, text parsing, citation formatting.
  Chrome Layer (Claude orchestration): Browser automation via Chrome MCP tools.

Usage:
  from dnd_library.manupatra_miner import cache, parser, citation
  cache.initialize_database()
  cache.cache_judgment(citation="(2023) 5 SCC 123", court="Supreme Court", ...)
  results = cache.search_cached("specific performance")
"""

from .cache import (
    initialize_database,
    cache_judgment,
    get_judgment,
    search_cached,
    get_cache_stats,
    list_recent,
    log_search,
)
from .parser import (
    parse_search_results,
    parse_judgment_page,
    extract_statutes_referred,
    extract_cases_referred,
    clean_judgment_text,
)
from .citation import (
    format_citation,
    format_for_pleading,
    format_for_argument,
    normalize_court_name,
    detect_citation_type,
)
from .judgment_export import (
    download_judgment,
    export_judgment_pdf,
    ensure_case_folder,
    list_case_folders,
)

__all__ = [
    # Cache
    "initialize_database", "cache_judgment", "get_judgment",
    "search_cached", "get_cache_stats", "list_recent", "log_search",
    # Parser
    "parse_search_results", "parse_judgment_page",
    "extract_statutes_referred", "extract_cases_referred", "clean_judgment_text",
    # Citation
    "format_citation", "format_for_pleading", "format_for_argument",
    "normalize_court_name", "detect_citation_type",
    # Judgment Export
    "download_judgment", "export_judgment_pdf",
    "ensure_case_folder", "list_case_folders",
]
