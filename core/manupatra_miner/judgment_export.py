"""
D&D Law Associates — Judgment Export with Highlighted Relevant Portions
Downloads cached judgments as PDFs with yellow-highlighted paragraphs
that are relevant to the legal issue at hand.

Uses PyMuPDF (fitz) for PDF generation with text and highlighting.

Folder structure:
  Legal Drafts/Case Files/<case_name>/Judgments/
    (2023) 5 SCC 123 - Ram Kumar vs Shyam Lal.pdf
"""

import os
import re
import fitz  # PyMuPDF


# ═══════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════

LEGAL_DRAFTS_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
CASE_FILES_DIR = os.path.join(LEGAL_DRAFTS_ROOT, "Case Files")


# ═══════════════════════════════════════════════════════════════
# PDF STYLING
# ═══════════════════════════════════════════════════════════════

FONT_NAME = "helv"          # Helvetica (built-in PDF font, close to Arial)
FONT_SIZE_TITLE = 14
FONT_SIZE_META = 10
FONT_SIZE_BODY = 11
FONT_SIZE_FOOTER = 8
LINE_HEIGHT = 14            # Points between lines for body text
PAGE_WIDTH = 595.28         # A4 width in points
PAGE_HEIGHT = 841.89        # A4 height in points
MARGIN_LEFT = 60
MARGIN_RIGHT = 60
MARGIN_TOP = 60
MARGIN_BOTTOM = 60
USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
HIGHLIGHT_COLOR = (1, 1, 0.6)  # Light yellow for highlights


# ═══════════════════════════════════════════════════════════════
# FOLDER MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def ensure_case_folder(case_name: str) -> str:
    """
    Create case folder structure if it doesn't exist.
    Returns path to the Judgments subfolder.

    Args:
        case_name: Case identifier (e.g., "Ram Kumar vs Shyam Lal")
    """
    # Sanitize folder name — remove characters invalid for filesystems
    safe_name = re.sub(r'[<>:"/\\|?*]', '', case_name).strip()
    safe_name = re.sub(r'\s+', ' ', safe_name)

    judgments_dir = os.path.join(CASE_FILES_DIR, safe_name, "Judgments")
    os.makedirs(judgments_dir, exist_ok=True)
    return judgments_dir


def get_case_folder(case_name: str) -> str:
    """Get existing case folder path (returns None if not exists)."""
    safe_name = re.sub(r'[<>:"/\\|?*]', '', case_name).strip()
    safe_name = re.sub(r'\s+', ' ', safe_name)
    path = os.path.join(CASE_FILES_DIR, safe_name, "Judgments")
    return path if os.path.exists(path) else None


def list_case_folders() -> list:
    """List all case folders and their judgment files."""
    if not os.path.exists(CASE_FILES_DIR):
        return []

    cases = []
    for case_dir in sorted(os.listdir(CASE_FILES_DIR)):
        case_path = os.path.join(CASE_FILES_DIR, case_dir)
        if not os.path.isdir(case_path):
            continue

        judgments_path = os.path.join(case_path, "Judgments")
        judgment_files = []
        if os.path.exists(judgments_path):
            judgment_files = [
                f for f in sorted(os.listdir(judgments_path))
                if f.endswith('.pdf')
            ]

        cases.append({
            "case_name": case_dir,
            "path": case_path,
            "judgments_path": judgments_path,
            "judgment_count": len(judgment_files),
            "judgment_files": judgment_files,
        })

    return cases


# ═══════════════════════════════════════════════════════════════
# RELEVANCE SCORING
# ═══════════════════════════════════════════════════════════════

def score_paragraph_relevance(paragraph: str, relevant_issue: str) -> float:
    """
    Score how relevant a paragraph is to the legal issue.
    Returns a score from 0.0 to 1.0.

    Uses keyword frequency matching — paragraphs with more
    matching keywords from the relevant_issue get higher scores.
    """
    if not paragraph or not relevant_issue:
        return 0.0

    para_lower = paragraph.lower()
    # Extract meaningful keywords (3+ chars, skip common words)
    stop_words = {
        'the', 'and', 'for', 'that', 'this', 'with', 'from', 'have', 'has',
        'was', 'were', 'been', 'are', 'not', 'but', 'shall', 'may', 'will',
        'which', 'such', 'under', 'upon', 'into', 'also', 'any', 'all',
        'its', 'his', 'her', 'their', 'there', 'here', 'said', 'court',
        'case', 'matter', 'order', 'dated', 'above', 'below',
    }

    keywords = [
        w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', relevant_issue)
        if w.lower() not in stop_words
    ]

    if not keywords:
        return 0.0

    # Count how many keywords appear in the paragraph
    matches = sum(1 for kw in keywords if kw in para_lower)
    score = matches / len(keywords)

    # Boost paragraphs that contain Section/Order references
    if re.search(r'[Ss]ection\s+\d+|[Oo]rder\s+\d+|[Aa]rticle\s+\d+', paragraph):
        if any(kw in para_lower for kw in keywords):
            score = min(1.0, score + 0.2)

    # Boost paragraphs with "held", "ratio", "principle", "law laid down"
    ratio_indicators = ['held that', 'we hold', 'principle', 'ratio', 'law laid down',
                        'settled law', 'well settled', 'observed that', 'opined that']
    if any(ind in para_lower for ind in ratio_indicators):
        if any(kw in para_lower for kw in keywords):
            score = min(1.0, score + 0.3)

    return score


def identify_relevant_paragraphs(full_text: str, relevant_issue: str,
                                  threshold: float = 0.3) -> list:
    """
    Split judgment text into paragraphs and identify which ones
    are relevant to the legal issue.

    Returns:
        List of (paragraph_text, is_highlighted, score) tuples
    """
    if not full_text:
        return []

    # Split into paragraphs — by numbered paras or double newlines
    # Manupatra judgments often have numbered paragraphs: "1.", "2.", etc.
    paragraphs = re.split(r'\n\s*\n|\n(?=\d+\.)', full_text)

    results = []
    for para in paragraphs:
        para = para.strip()
        if not para or len(para) < 10:
            continue

        score = score_paragraph_relevance(para, relevant_issue)
        is_highlighted = score >= threshold
        results.append((para, is_highlighted, score))

    return results


# ═══════════════════════════════════════════════════════════════
# PDF GENERATION WITH HIGHLIGHTS
# ═══════════════════════════════════════════════════════════════

def export_judgment_pdf(judgment: dict, relevant_issue: str, output_dir: str) -> str:
    """
    Export a judgment as a PDF with highlighted relevant paragraphs.

    Args:
        judgment: Dict from cache.get_judgment() with citation, court, parties,
                  bench, date_decided, headnotes, full_text, etc.
        relevant_issue: The legal issue to highlight (e.g.,
                        "readiness and willingness specific performance Section 10")
        output_dir: Directory to save the PDF

    Returns:
        Full path to the generated PDF file
    """
    citation = judgment.get("citation", "Unknown Citation")
    parties = judgment.get("parties", "Unknown")
    court = judgment.get("court", "")
    bench = judgment.get("bench", "")
    date_decided = judgment.get("date_decided", "")
    manu_id = judgment.get("manu_id", "")
    headnotes = judgment.get("headnotes", "")
    full_text = judgment.get("full_text", "")
    statutes = judgment.get("statutes_referred", "")
    cases_referred = judgment.get("cases_referred", "")

    # Generate safe filename
    safe_citation = re.sub(r'[<>:"/\\|?*().]', '', citation).strip()
    safe_parties = re.sub(r'[<>:"/\\|?*]', '', parties).strip()[:60]
    filename = f"{safe_citation} - {safe_parties}.pdf"
    filepath = os.path.join(output_dir, filename)

    # Create PDF document
    doc = fitz.open()

    # Track current position on current page
    current_page = None
    y_pos = MARGIN_TOP

    def new_page():
        nonlocal current_page, y_pos
        current_page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        y_pos = MARGIN_TOP
        return current_page

    def check_space(needed: float):
        """Start a new page if not enough space."""
        nonlocal y_pos
        if y_pos + needed > PAGE_HEIGHT - MARGIN_BOTTOM:
            new_page()

    def write_text(text: str, font_size: float = FONT_SIZE_BODY,
                   bold: bool = False, color: tuple = (0, 0, 0),
                   highlight: bool = False, indent: float = 0):
        """Write text with optional highlighting, handling line wrapping and page breaks."""
        nonlocal current_page, y_pos

        if not text:
            return

        fontname = FONT_NAME
        # Calculate approximate chars per line
        char_width = font_size * 0.5
        max_width = USABLE_WIDTH - indent
        chars_per_line = int(max_width / char_width) if char_width > 0 else 80

        # Word wrap
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test = current_line + (" " if current_line else "") + word
            if len(test) > chars_per_line:
                if current_line:
                    lines.append(current_line)
                current_line = word
            else:
                current_line = test
        if current_line:
            lines.append(current_line)

        line_spacing = font_size + 3

        for line in lines:
            check_space(line_spacing)

            x = MARGIN_LEFT + indent

            # Draw highlight background BEFORE text
            if highlight:
                rect = fitz.Rect(
                    MARGIN_LEFT,
                    y_pos - 2,
                    PAGE_WIDTH - MARGIN_RIGHT,
                    y_pos + font_size + 2
                )
                current_page.draw_rect(rect, color=HIGHLIGHT_COLOR, fill=HIGHLIGHT_COLOR)

            # Insert text
            current_page.insert_text(
                fitz.Point(x, y_pos + font_size),
                line,
                fontname=fontname,
                fontsize=font_size,
                color=color,
            )

            y_pos += line_spacing

    def write_separator():
        nonlocal y_pos
        check_space(20)
        current_page.draw_line(
            fitz.Point(MARGIN_LEFT, y_pos + 5),
            fitz.Point(PAGE_WIDTH - MARGIN_RIGHT, y_pos + 5),
            color=(0.6, 0.6, 0.6),
            width=0.5
        )
        y_pos += 15

    def add_page_numbers():
        """Add page numbers and footer to all pages."""
        total = len(doc)
        for i, page in enumerate(doc):
            # Page number
            page_text = f"Page {i + 1} of {total}"
            page.insert_text(
                fitz.Point(PAGE_WIDTH - MARGIN_RIGHT - 80, PAGE_HEIGHT - 25),
                page_text,
                fontname=FONT_NAME,
                fontsize=FONT_SIZE_FOOTER,
                color=(0.4, 0.4, 0.4),
            )
            # Footer
            footer = "Downloaded from Manupatra — D&D Law Associates"
            page.insert_text(
                fitz.Point(MARGIN_LEFT, PAGE_HEIGHT - 25),
                footer,
                fontname=FONT_NAME,
                fontsize=FONT_SIZE_FOOTER,
                color=(0.4, 0.4, 0.4),
            )

    # ── Start building PDF ──

    new_page()

    # ── Header: Case Title ──
    write_text(parties, font_size=FONT_SIZE_TITLE, bold=True)
    y_pos += 5

    # ── Metadata Block ──
    write_text(f"Citation: {citation}", font_size=FONT_SIZE_META, color=(0.2, 0.2, 0.2))
    if manu_id:
        write_text(f"MANU ID: {manu_id}", font_size=FONT_SIZE_META, color=(0.2, 0.2, 0.2))
    write_text(f"Court: {court}", font_size=FONT_SIZE_META, color=(0.2, 0.2, 0.2))
    if bench:
        write_text(f"Bench: {bench}", font_size=FONT_SIZE_META, color=(0.2, 0.2, 0.2))
    if date_decided:
        write_text(f"Decided On: {date_decided}", font_size=FONT_SIZE_META, color=(0.2, 0.2, 0.2))

    write_separator()

    # ── Highlight Legend ──
    if relevant_issue:
        write_text("RELEVANT ISSUE:", font_size=FONT_SIZE_META, bold=True, color=(0.6, 0, 0))
        write_text(relevant_issue, font_size=FONT_SIZE_META, color=(0.4, 0.4, 0.4), indent=10)
        # Show highlight indicator
        check_space(20)
        rect = fitz.Rect(MARGIN_LEFT, y_pos, MARGIN_LEFT + 60, y_pos + 12)
        current_page.draw_rect(rect, color=HIGHLIGHT_COLOR, fill=HIGHLIGHT_COLOR)
        current_page.insert_text(
            fitz.Point(MARGIN_LEFT + 65, y_pos + 10),
            " = Paragraphs relevant to the above issue",
            fontname=FONT_NAME, fontsize=FONT_SIZE_META, color=(0.4, 0.4, 0.4)
        )
        y_pos += 20
        write_separator()

    # ── Statutes Referred ──
    if statutes:
        write_text("ACTS/STATUTES REFERRED:", font_size=FONT_SIZE_META, bold=True, color=(0.3, 0.3, 0.3))
        write_text(statutes, font_size=FONT_SIZE_META, color=(0.3, 0.3, 0.3), indent=10)
        y_pos += 5

    # ── Cases Referred ──
    if cases_referred:
        write_text("CASES REFERRED:", font_size=FONT_SIZE_META, bold=True, color=(0.3, 0.3, 0.3))
        write_text(cases_referred, font_size=FONT_SIZE_META, color=(0.3, 0.3, 0.3), indent=10)
        y_pos += 5

    if statutes or cases_referred:
        write_separator()

    # ── Headnotes ──
    if headnotes:
        write_text("HEADNOTES:", font_size=FONT_SIZE_BODY, bold=True)
        y_pos += 3
        # Headnotes are always highlighted (they ARE the ratio)
        write_text(headnotes, font_size=FONT_SIZE_BODY, highlight=True)
        y_pos += 5
        write_separator()

    # ── Full Judgment Text with Highlights ──
    write_text("JUDGMENT", font_size=FONT_SIZE_TITLE, bold=True)
    y_pos += 8

    if full_text:
        # Score and highlight relevant paragraphs
        scored_paragraphs = identify_relevant_paragraphs(full_text, relevant_issue)

        highlight_count = 0
        for para_text, is_highlighted, score in scored_paragraphs:
            if is_highlighted:
                highlight_count += 1

            write_text(
                para_text,
                font_size=FONT_SIZE_BODY,
                highlight=is_highlighted,
            )
            y_pos += 5  # Spacing between paragraphs
    else:
        write_text("[No judgment text available in cache]", font_size=FONT_SIZE_BODY,
                   color=(0.5, 0.5, 0.5))

    # ── Add page numbers and footer ──
    add_page_numbers()

    # ── Save ──
    doc.save(filepath)
    doc.close()

    return filepath, highlight_count if full_text else 0


# ═══════════════════════════════════════════════════════════════
# HIGH-LEVEL WORKFLOW
# ═══════════════════════════════════════════════════════════════

def download_judgment(citation: str, case_name: str, relevant_issue: str = "") -> dict:
    """
    Complete workflow: retrieve cached judgment → create case folder → export highlighted PDF.

    Args:
        citation: Case citation to look up in cache
        case_name: Case name for folder creation
        relevant_issue: What to highlight (e.g., "readiness willingness specific performance")

    Returns:
        Dict with filepath, highlight_count, case_folder, status
    """
    from .cache import get_judgment

    # Step 1: Get judgment from cache
    judgment = get_judgment(citation)
    if not judgment:
        return {
            "status": "error",
            "error": f"Judgment not found in cache: {citation}. Mine from Manupatra first.",
        }

    # Step 2: Create case folder
    judgments_dir = ensure_case_folder(case_name)

    # Step 3: Export as highlighted PDF
    filepath, highlight_count = export_judgment_pdf(judgment, relevant_issue, judgments_dir)

    return {
        "status": "success",
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "case_folder": os.path.dirname(judgments_dir),
        "judgments_dir": judgments_dir,
        "citation": judgment.get("citation", citation),
        "parties": judgment.get("parties", ""),
        "highlight_count": highlight_count,
        "relevant_issue": relevant_issue,
        "file_size_kb": round(os.path.getsize(filepath) / 1024, 1),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "list":
        cases = list_case_folders()
        if not cases:
            print(f"No case folders found at: {CASE_FILES_DIR}")
        else:
            print(f"Case Files ({len(cases)} cases):")
            for c in cases:
                print(f"  {c['case_name']}: {c['judgment_count']} judgments")
                for f in c['judgment_files']:
                    print(f"    - {f}")
    else:
        print("Usage:")
        print("  python3 judgment_export.py list    # List case folders")
