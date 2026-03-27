"""
D&D Law Associates — Indian Legal Citation Formatter
Formats case citations in proper Indian legal format for use in
court pleadings, arguments, and legal opinions.

Supports: SCC, SCC OnLine, AIR, SCR, MANU, ALT, ALD, Cri LJ, ILR, MLJ
"""

import re
from .config import CITATION_PATTERNS, COURT_CODES


def format_citation(raw: str) -> str:
    """
    Normalize a raw citation string to standard Indian legal format.

    Examples:
        "2023 5 SCC 123"     → "(2023) 5 SCC 123"
        "AIR 2023 SC 789"    → "AIR 2023 SC 789"
        "MANU/SC/0123/2023"  → "MANU/SC/0123/2023"
    """
    if not raw:
        return raw

    raw = raw.strip()

    # Already properly formatted
    for pattern, fmt in CITATION_PATTERNS:
        if pattern.fullmatch(raw):
            return raw

    # Try to normalize SCC format: "2023 5 SCC 123" → "(2023) 5 SCC 123"
    scc_match = re.match(r'^(\d{4})\s+(\d+)\s+SCC\s+(\d+)$', raw)
    if scc_match:
        y, v, p = scc_match.groups()
        return f"({y}) {v} SCC {p}"

    # Try to normalize SCR format
    scr_match = re.match(r'^(\d{4})\s+(\d+)\s+SCR\s+(\d+)$', raw)
    if scr_match:
        y, v, p = scr_match.groups()
        return f"({y}) {v} SCR {p}"

    return raw


def format_for_pleading(citation: str, parties: str = "", court: str = "", year: str = "") -> str:
    """
    Format citation for use in court pleadings (Plaints, WS, Petitions).
    NOTE: Pleading Purity Rule — case law should NOT appear in Plaints/WS.
    This is for Appeals, Arguments, and Legal Opinions only.

    Format: Parties, Citation
    Example: Ram Kumar vs. Shyam Lal, (2023) 5 SCC 123
    """
    citation = format_citation(citation)

    if parties:
        # Clean up parties text
        parties = parties.strip().rstrip(",").rstrip(".")
        return f"{parties}, {citation}"

    return citation


def format_for_argument(citation: str, parties: str = "", court: str = "",
                        year: str = "", para: str = "") -> str:
    """
    Format citation for use in legal arguments with paragraph reference.
    Suitable for: Appeals, Revisions, Written Arguments, Legal Opinions.

    Format: Parties, Citation at para X
    Example: Ram Kumar vs. Shyam Lal, (2023) 5 SCC 123 at para 45
    """
    base = format_for_pleading(citation, parties, court, year)

    if para:
        return f"{base} at para {para}"

    return base


def format_for_list(citation: str, parties: str = "", ratio: str = "") -> str:
    """
    Format citation for a list of authorities / case law compilation.

    Format:
      1. Parties, Citation
         Ratio: [brief ratio text]
    """
    base = format_for_pleading(citation, parties)
    if ratio:
        return f"{base}\n   Ratio: {ratio}"
    return base


def normalize_court_name(raw: str) -> str:
    """
    Normalize court name to standard abbreviation.

    Examples:
        "Supreme Court of India" → "SC"
        "High Court of Andhra Pradesh" → "AP HC"
        "Bombay High Court" → "Bom HC"
        "National Consumer Disputes Redressal Commission" → "NCDRC"
    """
    if not raw:
        return ""

    raw_clean = raw.strip().lower()

    # Check exact matches in COURT_CODES
    for key, info in COURT_CODES.items():
        if raw_clean == key:
            return info["abbr"]
        if raw_clean == info["name"].lower():
            return info["abbr"]
        if raw_clean == info["code"].lower():
            return info["abbr"]

    # Partial matches
    if "supreme court" in raw_clean:
        return "SC"

    # "High Court of X" pattern
    hc_match = re.search(r'high\s+court\s+(?:of\s+)?(\w[\w\s&]+)', raw_clean)
    if hc_match:
        state = hc_match.group(1).strip()
        for key, info in COURT_CODES.items():
            if state in info["name"].lower():
                return info["abbr"]
        return f"{state.title()} HC"

    # "X High Court" pattern
    hc_match2 = re.search(r'(\w[\w\s&]+?)\s+high\s+court', raw_clean)
    if hc_match2:
        state = hc_match2.group(1).strip()
        for key, info in COURT_CODES.items():
            if state in info["name"].lower():
                return info["abbr"]
        return f"{state.title()} HC"

    # Tribunal patterns
    tribunal_map = {
        "ncdrc": "NCDRC", "nclt": "NCLT", "nclat": "NCLAT",
        "drt": "DRT", "drat": "DRAT", "cat": "CAT",
        "itat": "ITAT", "sat": "SAT", "rera": "RERA",
    }
    for key, abbr in tribunal_map.items():
        if key in raw_clean:
            return abbr

    return raw.strip()


def detect_citation_type(text: str) -> str:
    """
    Detect the type of citation format in text.

    Returns: "SCC", "SCC_ONLINE", "AIR", "SCR", "MANU", "ALT", "ALD",
             "SCC_CRI", "CRI_LJ", "ILR", "MLJ", "CDJ", or "UNKNOWN"
    """
    if not text:
        return "UNKNOWN"

    for pattern, fmt in CITATION_PATTERNS:
        if pattern.search(text):
            return fmt

    return "UNKNOWN"


def extract_all_citations(text: str) -> list:
    """
    Extract ALL citations from a block of text.
    Useful for building a table of authorities.

    Returns:
        List of dicts: [{citation, type, position}, ...]
    """
    if not text:
        return []

    citations = []
    seen = set()

    for pattern, fmt in CITATION_PATTERNS:
        for match in pattern.finditer(text):
            cit = match.group().strip()
            if cit not in seen:
                seen.add(cit)
                citations.append({
                    "citation": cit,
                    "type": fmt,
                    "position": match.start(),
                })

    # Sort by position in text
    citations.sort(key=lambda x: x["position"])
    return citations


def format_table_of_authorities(cases: list) -> str:
    """
    Format a list of cases into a Table of Authorities.

    Args:
        cases: List of dicts with at least {citation, parties}.
               Optional: {court, year, para, ratio}

    Returns:
        Formatted table as string.
    """
    if not cases:
        return "No authorities to list."

    lines = [
        "TABLE OF AUTHORITIES",
        "=" * 50,
        ""
    ]

    for i, case in enumerate(cases, 1):
        citation = format_citation(case.get("citation", ""))
        parties = case.get("parties", "")
        court = case.get("court", "")
        para = case.get("para", "")
        ratio = case.get("ratio", "")

        entry = f"{i}. "
        if parties:
            entry += f"{parties}, "
        entry += citation

        if court:
            entry += f" ({normalize_court_name(court)})"

        if para:
            entry += f" at para {para}"

        lines.append(entry)

        if ratio:
            lines.append(f"   Ratio: {ratio}")

        lines.append("")

    return "\n".join(lines)
