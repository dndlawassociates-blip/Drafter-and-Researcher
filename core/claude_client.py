"""Claude API Client — AI-powered legal drafting and research."""

import anthropic
from typing import Optional


def get_client(api_key: str) -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=api_key)


SYSTEM_PROMPT = """You are a 40-year senior advocate practicing in Indian courts, specializing in AP/Telangana jurisdiction. You work for D&D Law Associates (Advocates: DEEPAK ARAVIND.K & DEEPTHI.G, Visakhapatnam).

MANDATORY RULES:
1. Draft in formal legal English with proper honorifics (Hon'ble Court, Ld. Counsel)
2. ALL monetary amounts in Indian format: Rs.X,XX,XXX/- (Rupees _____ only) — Lakhs/Crores ONLY, NEVER Millions/Billions
3. ZERO case law in Plaints, Written Statements, Consumer Complaints, Family Petitions (case law ONLY in Applications, Appeals, Bail, Writs, Arguments)
4. Consecutive paragraph numbering — never restart mid-document
5. Verification clause: split Personal Knowledge from Information & Belief paragraphs
6. Supporting affidavit is MANDATORY for all AP/Telangana court filings
7. Letterhead ONLY for Legal Notices (Module E). NEVER on court pleadings
8. Use NEW criminal law: BNS (not IPC), BNSS (not CrPC), BSA (not Evidence Act)
9. Schedule Property: 4 boundaries (East/West/North/South) + survey number + admeasurement
10. Document list as Annexures (NOT Exhibits — Exhibits are marked at trial)

AP COURT HIERARCHY:
- Junior Civil Judge: Up to Rs.3 Lakh
- Senior Civil Judge: Rs.3 Lakh - Rs.50 Lakh
- District Judge: Above Rs.50 Lakh
- Family Court: Exclusive jurisdiction for matrimonial matters
- Consumer Forum: Exclusive for consumer disputes
- DRT: Exclusive for debts Rs.10 Lakh+ (bar on civil court)
- MACT: Exclusive for motor accident claims

D&D LAW ASSOCIATES:
Advocates: DEEPAK ARAVIND.K | DEEPTHI.G
Door No. 49-20-5/c, Lalithanagar, R.K. Nagar, Opp Roshni Residency, Visakhapatnam-16, AP
Email: dndlawassociates@gmail.com | Mobile: 7382398999"""


def chat(api_key: str, prompt: str, system: str = None) -> str:
    """Send a message to Claude and get a response."""
    try:
        client = get_client(api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            system=system or SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except anthropic.AuthenticationError:
        return "ERROR: Invalid API key. Please check your Anthropic API key."
    except anthropic.RateLimitError:
        return "ERROR: Rate limit exceeded. Please wait a moment and try again."
    except Exception as e:
        return f"ERROR: {str(e)}"


def draft_document(api_key: str, prompt: str) -> str:
    """Generate a legal draft using Claude."""
    enhanced_prompt = f"""Draft the following legal document. Follow ALL chamber protocol rules strictly.
Output the complete draft ready for filing — do not skip any section.

{prompt}

IMPORTANT: Output the COMPLETE draft from cause title to signature block. Include:
- Full cause title with proper court designation
- All mandatory sections
- Prayer clause with specific reliefs
- Verification clause (Personal Knowledge vs Information & Belief split)
- Supporting affidavit (mandatory for AP courts)
- Document list as numbered Annexures"""

    return chat(api_key, enhanced_prompt)


def research_query(api_key: str, query: str) -> str:
    """Research a legal question using Claude."""
    enhanced_prompt = f"""As a 40-year senior advocate, research and answer the following legal question thoroughly:

{query}

Provide:
1. Applicable statutory provisions with exact section numbers
2. Key case law with full citations (Party vs Party, Year, Reporter, Page)
3. Practical advice for the advocate handling this matter
4. Any risks or pitfalls to watch out for
5. Recommended approach

Use BNS/BNSS/BSA (not IPC/CrPC/Evidence Act) for criminal law references."""

    return chat(api_key, enhanced_prompt)


def analyze_case(api_key: str, facts: str) -> str:
    """Analyze case strength and provide strategy."""
    enhanced_prompt = f"""As a 40-year senior advocate, analyze this case and provide strategic advice:

CASE FACTS:
{facts}

Provide a COMPLETE analysis:
1. STRENGTH RATING: Strong / Moderate / Weak (with reasons)
2. STRONGEST POINTS — What works in the client's favor
3. WEAKEST POINTS — Where the client is vulnerable
4. BEST FORUM — Which court/tribunal to approach (civil/consumer/DRT/family/MACT/RERA/NCLT)
5. RECOMMENDED RELIEFS — What to pray for
6. INTERIM RELIEF — Any urgent interim orders needed?
7. LIMITATION — Is the case within time?
8. OPPOSING ARGUMENTS — What will the other side argue?
9. COUNTER-STRATEGY — How to handle opposing arguments
10. SETTLEMENT — Is ADR/mediation advisable?
11. STEP-BY-STEP ACTION PLAN

Be brutally honest. If the case is weak, say so."""

    return chat(api_key, enhanced_prompt)


def review_draft(api_key: str, draft: str, doc_type: str = "legal document") -> str:
    """Review a legal draft for errors and improvements."""
    enhanced_prompt = f"""As a 40-year senior advocate, review this {doc_type} using the 10-Point Senior Advocate Scrutiny Checklist:

DRAFT TO REVIEW:
{draft}

CHECK ALL 10 POINTS:
1. JURISDICTIONAL PRECISION — Territorial + pecuniary + subject-matter correct?
2. LIMITATION VIGILANCE — Correct article, within time?
3. PLEADING PURITY — No case law in pleadings? (Only in applications/appeals)
4. CAUSE OF ACTION — Specific dates, places, events?
5. SCHEDULE PROPERTY — 4 boundaries, survey number, admeasurement?
6. MONETARY AMOUNTS — All in Indian format (Lakhs/Crores)?
7. AFFIDAVIT — Included for AP court filing?
8. VERIFICATION — Personal Knowledge vs Information & Belief split?
9. NO ASSUMPTIONS — All facts verified?
10. PROFESSIONAL LANGUAGE — Formal legal English? Proper honorifics?

OUTPUT:
- List of errors (critical and minor)
- Suggested improvements
- Missing elements
- Overall: Ready / Needs Revision / Major Rewrite"""

    return chat(api_key, enhanced_prompt)
