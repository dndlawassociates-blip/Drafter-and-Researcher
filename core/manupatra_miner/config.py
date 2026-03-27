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
LOGIN_URL = f"{BASE_URL}/homepopup.aspx"
HOME_URL = f"{BASE_URL}/pers/Personalized.aspx"
MANU_SEARCH_URL = f"{BASE_URL}/ESP/ManuSearchFilter.aspx"
LEGAL_SEARCH_URL = f"{BASE_URL}/Search/AdvanceSearch.aspx"
CITATION_SEARCH_URL = f"{BASE_URL}/Search/CitationSearch.aspx"
JUDGMENT_URL = f"{BASE_URL}/pers/viewdoc.aspx"

# Alternative domains (manupatrafast.com redirects from these)
ALT_URLS = [
    "https://manupatra.com",
    "https://www.manupatra.com",
    "https://www.manupatra.ai",
]

# ═══════════════════════════════════════════════════════════════
# CSS SELECTORS (Calibrate during first live session)
# ═══════════════════════════════════════════════════════════════

SELECTOR_VERSION = "1.0-calibrated"
SELECTOR_LAST_CALIBRATED = "2026-03-27"

# ═══════════════════════════════════════════════════════════════
# FRAME STRUCTURE (Critical — Manupatra uses nested framesets)
# ═══════════════════════════════════════════════════════════════
# Main frameset (Personalized.aspx):
#   ├── frameheader  → phead.aspx (top nav bar: Home, Manu Search, Legal Search, Citation, etc.)
#   ├── framesearch  → pMainBody.aspx (main area, ALSO a frameset!)
#   │   ├── frametoc    → treeview/treeview.aspx (left sidebar: court/topic tree)
#   │   ├── frametools  → pers/tools.aspx (toolbar above content)
#   │   ├── framebody   → ESP/ManuSearchFilter.aspx (search form / results / judgment viewer)
#   │   └── framenotepad → (empty)
#   ├── framebottom  → pfoot.aspx (footer)
#   └── framerefresh → refresh.aspx (session keepalive)
#
# KEY INSIGHT: The actual content (search form, results, judgments) is always in:
#   window.frames['framesearch'].frames['framebody']
# The framebody URL changes as user navigates:
#   - Search form: ESP/ManuSearchFilter.aspx
#   - Search results: SearchResult page
#   - Judgment view: pers/viewdoc.aspx
#
# IMPORTANT: get_page_text and read_page DON'T work on framesets.
# Use JavaScript to extract text from the inner frame:
#   window.frames['framesearch'].frames['framebody'].document.body.innerText
# Or navigate directly to the inner frame URL in a separate tab.

FRAME_HIERARCHY = {
    "header": "frameheader",       # phead.aspx
    "search_area": "framesearch",  # pMainBody.aspx (contains nested frames)
    "content": "framebody",        # The actual content frame (inside framesearch)
    "toc": "frametoc",             # Left sidebar
    "tools": "frametools",         # Toolbar
}

# JavaScript to extract text from the content frame (use with javascript_tool)
JS_EXTRACT_TEXT = """
try {
    var sf = window.frames['framesearch'];
    var bf = sf.frames['framebody'];
    bf.document.body.innerText;
} catch(e) { 'Error: ' + e.message; }
"""

SELECTORS = {
    # ── Manu Search Page (ESP/ManuSearchFilter.aspx) ──
    "search_box": "#txtSearchBox",
    "search_button": "#btnSearch, p.btnsearch",
    "search_type_dropdown": "#ddlSearchType",    # Free Text / Title / etc.
    "exclude_words": "#txtNegativeSearch",
    "refine_box": "#txtRefineBox",
    "refine_type": "#ddlRefineType",
    "login_indicator": "Welcome",                # Text on page after login

    # Search In radio buttons
    "radio_freetext": "#rbtfreetext",
    "radio_title": "#rbttitle",
    "radio_citation": "#rbtcitation",
    "radio_exactphrase": "#rbtexactphrase",

    # Boolean operations
    "radio_bool_auto": "#rbtauto",
    "radio_bool_and": "#rband",
    "radio_bool_or": "#rbtor",

    # ── Legal Search / Advanced Search (Search/AdvanceSearch.aspx) ──
    "adv_appellant": "#txtAppellant",            # Appellant/Respondent name
    "adv_judges": "#txtJudges",                  # Judge name
    "adv_casenote": "#txtCaseNote",              # Case note text
    "adv_subject": "#drpSubject",                # Subject dropdown
    "adv_sub_subject": "#txtSubSubject",         # Sub-subject text
    "adv_bool_type": "#ddlType",                 # Boolean type for sub-subject
    "adv_case_category": "#CaseCategory",        # Case category dropdown
    "adv_case_subcategory": "#CaseSubCategory",  # Case sub-category dropdown
    "adv_disposition": "#drpDisposition",        # Disposition dropdown
    "adv_date_on": "input[name='1'][value='on']",
    "adv_date_range": "input[name='1'][value='range']",
    "adv_search_type": "RadioButtonList1",       # Radio: 0=AdvSearch, 1=Section, 2=RelSection, 3=CaseNo, 4=Bench, 5=SearchByBench

    # ── Citation Search (Search/CitationSearch.aspx) ──
    "cit_publisher": "#drpPublisher",            # Publisher dropdown (SCC, AIR, etc.)
    "cit_year": "#txtEnterYear",
    "cit_volume": "#txtVolumeNumber",
    "cit_page": "#txtPageNumber",
    "cit_court": "#drpCourt",                    # Court dropdown
    # Manu Citation tab
    "cit_manu_publisher": "#drpPublishermanu",
    "cit_manu_year": "#txtEnterYearmanu",
    "cit_manu_volume": "#txtVolumeNumbermanu",
    "cit_manu_page": "#txtPageNumbermanu",

    # ── Search Results Page ──
    # Results load in framebody. Use JS_EXTRACT_TEXT to get text.
    # Results are numbered: "1. Case Name (Date - Court)"
    # Filter sidebar: Court, Keywords, Subject, Judge, Period, Document Type

    # ── Judgment Detail Page (pers/viewdoc.aspx) ──
    # Judgment text is in framebody. Use JS_EXTRACT_TEXT to get full text.
    # Tabs visible at top: All, Subject, Coram, Casenote, Cases Referred,
    #   Acts, Citing Reference, Status, Overruled/Reversed, References, Judgment
    # Text structure (parsed by parser.py):
    #   MANU/XX/NNNN/YYYY
    #   Neutral Citation: ...
    #   IN THE [COURT NAME]
    #   [Case Number]
    #   Decided On: DD.MM.YYYY
    #   [Appellant] Vs. [Respondent]
    #   Hon'ble Judges/Coram: ...
    #   Subject: ...
    #   Acts/Rules/Orders: ...
    #   Cases Referred: ...
    #   [JUDGMENT TEXT]

    # ── Header Navigation (phead.aspx) ──
    "nav_home": "javascript:OpenWin('RedirectToManuSearch.aspx')",
    "nav_manu_search": "javascript:OpenWin('RedirectToManuSearch.aspx')",
    "nav_legal_search": "javascript:OpenWin('../Search/AdvanceSearch.aspx')",
    "nav_citation": "javascript:OpenWin('../Search/CitationSearch.aspx')",
    "nav_search_history": "javascript:OpenWin('../Search/SearchHistory.aspx')",
    "nav_results": "Results",
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
MANUPATRA CASE LAW MINING — CALIBRATED CHROME WORKFLOW (v1.0)

CRITICAL: Manupatra uses NESTED FRAMESETS. Standard get_page_text and read_page
DO NOT WORK on the main page. Use JavaScript extraction instead.

Step 1: Navigate to Manupatra
  → navigate(url="https://www.manupatrafast.com/pers/Personalized.aspx")
  → Wait 2 seconds for frames to load
  → Take screenshot to verify login (look for "Welcome [name]")
  → If login page shown: inform user to log in manually (password required)

Step 2: Search (Manu Search — main search box)
  → Click on search box at approximate coordinates (center of "Enter Text" field)
  → Type the search query: computer(action="type", text="{query}")
  → Click the "Search" button (red button to the right)
  → Wait 5 seconds for results to load

Step 3: Extract Results (from inner frame via JavaScript)
  → Use javascript_tool to extract text from the content frame:
    window.frames['framesearch'].frames['framebody'].document.body.innerText
  → Parse the result list: numbered entries like "1. Case Name (Date - Court)"
  → Note the filter sidebar for court/period/subject filtering

Step 4: Open Judgment
  → Click on the case title link in the results (use coordinates from screenshot)
  → Wait 4 seconds for judgment to load in framebody

Step 5: Extract Full Judgment (via JavaScript)
  → Use javascript_tool to extract from content frame:
    window.frames['framesearch'].frames['framebody'].document.body.innerText
  → The text follows this structure:
    MANU/XX/NNNN/YYYY
    Neutral Citation: ...
    IN THE [COURT NAME]
    [Case Number]
    Decided On: DD.MM.YYYY
    [Appellant] Vs. [Respondent]
    Hon'ble Judges/Coram: [bench]
    Subject: [subject]
    Acts/Rules/Orders: [statutes list]
    Cases Referred: [cited cases]
    [JUDGMENT / ORDER text]

Step 6: Cache
  → Call manupatra_cache_judgment MCP tool with parsed data
  → Judgment is now available offline via manupatra_search_cached

Step 7: Navigate Back to Results
  → Click browser back or use the "Results" link in header nav
  → Repeat Steps 4-6 for additional relevant judgments

ALTERNATIVE: Legal Search (Advanced)
  → Navigate to: https://www.manupatrafast.com/Search/AdvanceSearch.aspx
  → This opens OUTSIDE frames — standard tools work here
  → Fields: #txtAppellant, #txtJudges, #txtCaseNote, #drpSubject, etc.
  → More precise than Manu Search for targeted case law mining

ALTERNATIVE: Citation Search
  → Navigate to: https://www.manupatrafast.com/Search/CitationSearch.aspx
  → Fields: #drpPublisher (SCC/AIR/etc.), #txtEnterYear, #txtVolumeNumber, #txtPageNumber
  → Use when you have a specific citation to look up
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
