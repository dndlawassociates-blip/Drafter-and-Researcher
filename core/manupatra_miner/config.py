"""
D&D Law Associates — Manupatra Mining Configuration
URLs, CSS selectors, court codes, citation patterns, and cache settings.

Selector Calibration:
  Selectors are best-guess defaults. On first live browser session,
  use Chrome MCP `read_page(filter="interactive")` to discover actual
  element IDs/classes, then update SELECTORS below.
  Increment SELECTOR_VERSION after each calibration.
"""

import os

# ═══════════════════════════════════════════════════════════════
# MANUPATRA URLs
# ═══════════════════════════════════════════════════════════════

BASE_URL = "https://www.manupatrafast.com"
SEARCH_URL = f"{BASE_URL}/SearchResult/SearchResult.aspx"
ADVANCED_SEARCH_URL = f"{BASE_URL}/Defaults/AdvancedSearch.aspx"
HOME_URL = f"{BASE_URL}/"

# Alternative domains (Manupatra has multiple entry points)
ALT_URLS = [
    "https://manupatra.com",
    "https://www.manupatra.com",
    "https://manupatrafast.in",
]

# ═══════════════════════════════════════════════════════════════
# CSS SELECTORS (Calibrate during first live session)
# ═══════════════════════════════════════════════════════════════

SELECTOR_VERSION = "0.1-uncalibrated"
SELECTOR_LAST_CALIBRATED = None  # Set to ISO date after first calibration

SELECTORS = {
    # ── Home / Search Page ──
    "search_box": "input[type='text'][name*='search'], input[type='text'][name*='Search'], #txtSearch, #txtGlobalSearch",
    "search_button": "input[type='submit'], button[type='submit'], #btnSearch, #btnGlobalSearch",
    "login_indicator": ".user-name, .username, #lblUserName, .logged-in",

    # ── Search Results Page ──
    "result_container": ".search-result, .searchresult, .result-item, .search_result_row",
    "result_title": ".search-result a, .result-title a, .searchresult a.case-link",
    "result_citation": ".citation, .cite, .case-citation, span.citation",
    "result_court": ".court-name, .court, span.court",
    "result_date": ".decision-date, .date, span.date",
    "result_snippet": ".snippet, .result-text, .search-snippet",
    "result_link": ".search-result a[href], .result-title a[href]",
    "pagination_next": ".next, .pagination a.next, a[title='Next']",
    "total_results": ".result-count, .total-results, #lblTotalResults",

    # ── Judgment Detail Page ──
    "judgment_full_text": "#divFullText, #divJudgment, .judgment-text, .full-text, #ContentPlaceHolder1_divContent",
    "judgment_citation": ".case-citation, .judgment-citation, #lblCitation",
    "judgment_court": ".court-name, .judgment-court, #lblCourt",
    "judgment_bench": ".bench, .judges, .coram, #lblBench",
    "judgment_date": ".judgment-date, .decided-on, #lblDate",
    "judgment_parties": ".case-title, .parties, #lblParties",
    "judgment_headnotes": ".headnote, .head-note, #divHeadNote",
    "judgment_acts": ".acts-referred, .statutes, #divActsReferred",
    "judgment_cases_cited": ".cases-referred, .cases-cited, #divCasesReferred",

    # ── Advanced Search Filters ──
    "court_dropdown": "#ddlCourt, select[name*='Court'], select[name*='court']",
    "year_from": "#txtYearFrom, input[name*='yearFrom'], input[name*='YearFrom']",
    "year_to": "#txtYearTo, input[name*='yearTo'], input[name*='YearTo']",
    "section_field": "#txtSection, input[name*='section'], input[name*='Section']",
    "act_field": "#txtAct, input[name*='act'], input[name*='Act']",
}

# ═══════════════════════════════════════════════════════════════
# COURT CODES (Manupatra internal identifiers)
# ═══════════════════════════════════════════════════════════════

COURT_CODES = {
    # Supreme Court
    "supreme_court": {"code": "SC", "name": "Supreme Court of India", "abbr": "SC"},
    "sc": {"code": "SC", "name": "Supreme Court of India", "abbr": "SC"},

    # High Courts (commonly used)
    "andhra_pradesh": {"code": "APHC", "name": "High Court of Andhra Pradesh", "abbr": "AP HC"},
    "ap": {"code": "APHC", "name": "High Court of Andhra Pradesh", "abbr": "AP HC"},
    "telangana": {"code": "TSHC", "name": "High Court of Telangana", "abbr": "TS HC"},
    "ts": {"code": "TSHC", "name": "High Court of Telangana", "abbr": "TS HC"},
    "delhi": {"code": "DLHC", "name": "High Court of Delhi", "abbr": "Del HC"},
    "bombay": {"code": "BCHC", "name": "Bombay High Court", "abbr": "Bom HC"},
    "madras": {"code": "MDHC", "name": "Madras High Court", "abbr": "Mad HC"},
    "calcutta": {"code": "CLHC", "name": "Calcutta High Court", "abbr": "Cal HC"},
    "karnataka": {"code": "KAHC", "name": "High Court of Karnataka", "abbr": "Kar HC"},
    "kerala": {"code": "KLHC", "name": "High Court of Kerala", "abbr": "Ker HC"},
    "allahabad": {"code": "ALHC", "name": "High Court of Allahabad", "abbr": "All HC"},
    "punjab_haryana": {"code": "PHHC", "name": "Punjab & Haryana High Court", "abbr": "P&H HC"},
    "gujarat": {"code": "GJHC", "name": "Gujarat High Court", "abbr": "Guj HC"},
    "rajasthan": {"code": "RJHC", "name": "Rajasthan High Court", "abbr": "Raj HC"},
    "jharkhand": {"code": "JHHC", "name": "Jharkhand High Court", "abbr": "Jha HC"},
    "chhattisgarh": {"code": "CGHC", "name": "Chhattisgarh High Court", "abbr": "CG HC"},
    "patna": {"code": "PTHC", "name": "Patna High Court", "abbr": "Pat HC"},
    "gauhati": {"code": "GHHC", "name": "Gauhati High Court", "abbr": "Gau HC"},
    "orissa": {"code": "ORHC", "name": "Orissa High Court", "abbr": "Ori HC"},
    "himachal_pradesh": {"code": "HPHC", "name": "HP High Court", "abbr": "HP HC"},
    "uttarakhand": {"code": "UKHC", "name": "Uttarakhand High Court", "abbr": "Utk HC"},
    "manipur": {"code": "MNHC", "name": "Manipur High Court", "abbr": "Man HC"},
    "meghalaya": {"code": "MGHC", "name": "Meghalaya High Court", "abbr": "Meg HC"},
    "tripura": {"code": "TRHC", "name": "Tripura High Court", "abbr": "Tri HC"},
    "sikkim": {"code": "SKHC", "name": "Sikkim High Court", "abbr": "Sik HC"},

    # Tribunals
    "nclat": {"code": "NCLAT", "name": "NCLAT", "abbr": "NCLAT"},
    "nclt": {"code": "NCLT", "name": "NCLT", "abbr": "NCLT"},
    "ncdrc": {"code": "NCDRC", "name": "National Consumer Disputes Redressal Commission", "abbr": "NCDRC"},
    "drt": {"code": "DRT", "name": "Debt Recovery Tribunal", "abbr": "DRT"},
    "drat": {"code": "DRAT", "name": "Debt Recovery Appellate Tribunal", "abbr": "DRAT"},
    "rera": {"code": "RERA", "name": "Real Estate Regulatory Authority", "abbr": "RERA"},
    "cat": {"code": "CAT", "name": "Central Administrative Tribunal", "abbr": "CAT"},
    "itat": {"code": "ITAT", "name": "Income Tax Appellate Tribunal", "abbr": "ITAT"},
    "sat": {"code": "SAT", "name": "Securities Appellate Tribunal", "abbr": "SAT"},

    # All courts
    "all": {"code": "ALL", "name": "All Courts", "abbr": "All"},
}

# ═══════════════════════════════════════════════════════════════
# CITATION PATTERNS (regex for detecting citation formats)
# ═══════════════════════════════════════════════════════════════

import re

CITATION_PATTERNS = [
    # (2023) 5 SCC 123
    (re.compile(r'\((\d{4})\)\s*(\d+)\s*SCC\s+(\d+)'), "SCC"),
    # 2023 SCC OnLine SC 456
    (re.compile(r'(\d{4})\s+SCC\s+OnLine\s+(\w+)\s+(\d+)'), "SCC_ONLINE"),
    # AIR 2023 SC 789
    (re.compile(r'AIR\s+(\d{4})\s+(\w+)\s+(\d+)'), "AIR"),
    # (2023) 1 SCR 100
    (re.compile(r'\((\d{4})\)\s*(\d+)\s*SCR\s+(\d+)'), "SCR"),
    # MANU/SC/0123/2023
    (re.compile(r'MANU/(\w+)/(\d+)/(\d{4})'), "MANU"),
    # 2023 (5) ALT 123
    (re.compile(r'(\d{4})\s*\((\d+)\)\s*ALT\s+(\d+)'), "ALT"),
    # 2023 (2) ALD 456
    (re.compile(r'(\d{4})\s*\((\d+)\)\s*ALD\s+(\d+)'), "ALD"),
    # (2023) 4 SCC (Cri) 123
    (re.compile(r'\((\d{4})\)\s*(\d+)\s*SCC\s*\(Cri\)\s*(\d+)'), "SCC_CRI"),
    # 2023 Cri LJ 789
    (re.compile(r'(\d{4})\s+Cri\.?\s*L\.?J\.?\s+(\d+)'), "CRI_LJ"),
    # ILR 2023 KAR 456
    (re.compile(r'ILR\s+(\d{4})\s+(\w+)\s+(\d+)'), "ILR"),
    # (2023) 2 MLJ 100
    (re.compile(r'\((\d{4})\)\s*(\d+)\s*MLJ\s+(\d+)'), "MLJ"),
    # CDJ 2023 SC 123
    (re.compile(r'CDJ\s+(\d{4})\s+(\w+)\s+(\d+)'), "CDJ"),
]

# ═══════════════════════════════════════════════════════════════
# STATUTE REFERENCE PATTERNS (for extracting from judgment text)
# ═══════════════════════════════════════════════════════════════

STATUTE_PATTERNS = [
    # Section X of Y Act
    re.compile(r'[Ss]ection\s+(\d+[A-Za-z]*(?:\s*\(\d+\))?(?:\s*\([a-z]\))?)\s+of\s+(?:the\s+)?(.+?)(?:\s*,|\s*\.|\s+read|\s+r/w|\s+and|\s+or|\s*$)', re.MULTILINE),
    # S. X of Y Act
    re.compile(r'[Ss]\.\s*(\d+[A-Za-z]*(?:\s*\(\d+\))?)\s+of\s+(?:the\s+)?(.+?)(?:\s*,|\s*\.|\s+read|\s*$)', re.MULTILINE),
    # Order X Rule Y CPC
    re.compile(r'[Oo]rder\s+(\w+)\s+[Rr]ule\s+(\d+(?:\s*\(\d+\))?)\s+(?:of\s+)?(?:the\s+)?(?:CPC|Code of Civil Procedure|C\.P\.C\.)', re.MULTILINE),
    # Article X of Constitution
    re.compile(r'[Aa]rticle\s+(\d+[A-Za-z]*(?:\s*\(\d+\))?)\s+of\s+(?:the\s+)?Constitution', re.MULTILINE),
    # u/s X of Y Act
    re.compile(r'u/[sS]\s*\.?\s*(\d+[A-Za-z]*(?:\s*\(\d+\))?)\s+(?:of\s+)?(?:the\s+)?(.+?)(?:\s*,|\s*\.|\s*$)', re.MULTILINE),
]

# ═══════════════════════════════════════════════════════════════
# CACHE SETTINGS
# ═══════════════════════════════════════════════════════════════

CACHE_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "manupatra_cache.db")
CACHE_MAX_AGE_DAYS = 90  # Judgments don't change; 90-day cache is generous

# ═══════════════════════════════════════════════════════════════
# CHROME MINING WORKFLOW INSTRUCTIONS
# ═══════════════════════════════════════════════════════════════

MINING_WORKFLOW = """
MANUPATRA CASE LAW MINING — CHROME WORKFLOW

Step 1: Navigate to Manupatra
  → Use Chrome MCP: navigate(url="{base_url}")
  → Verify login: use find("search") to locate search box
  → If not logged in: inform user to log in first

Step 2: Search
  → Use find("search box") to locate the search input
  → Use form_input(ref=<ref>, value="{query}") to enter query
  → Use computer(action="left_click", ref=<search_button>) to submit
  → Use computer(action="wait", duration=3) for results to load

Step 3: Extract Results
  → Use get_page_text to extract the search results page
  → Parse results to identify relevant cases
  → Note citation, court, date for each result

Step 4: Open Judgment
  → Use find("<case title>") to locate the result link
  → Use computer(action="left_click", ref=<ref>) to open
  → Use computer(action="wait", duration=3) for judgment to load

Step 5: Extract Judgment
  → Use get_page_text to extract the full judgment text
  → Parse: citation, court, bench, date, parties, headnotes, full text

Step 6: Cache
  → Call manupatra_cache_judgment MCP tool with extracted data
  → Judgment is now available offline via manupatra_search_cached

Step 7: Report
  → Present formatted citations to user
  → Include relevant headnotes/ratio for the legal issue
"""


def get_mining_instructions(query: str, court: str = "", year: str = "") -> str:
    """Generate Chrome mining workflow instructions for a specific query."""
    instructions = MINING_WORKFLOW.format(
        base_url=HOME_URL,
        query=query
    )

    if court:
        court_info = COURT_CODES.get(court.lower(), {})
        if court_info:
            instructions += f"\nCourt Filter: {court_info.get('name', court)} ({court_info.get('code', '')})"
            instructions += f"\n  → After entering search query, look for court dropdown/filter"
            instructions += f"\n  → Select: {court_info.get('name', court)}"

    if year:
        instructions += f"\nYear Filter: {year}"
        instructions += f"\n  → After entering search query, look for year/date filter"
        instructions += f"\n  → Enter year range: {year}"

    return instructions
