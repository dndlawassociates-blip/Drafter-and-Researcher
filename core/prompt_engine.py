"""Expert Legal Prompt Engine — 50+ chamber-grade prompts for D&D Law Associates."""

PROMPT_CATEGORIES = {
    "drafting": "Legal Drafting Prompts",
    "research": "Legal Research Prompts",
    "analysis": "Case Analysis & Strategy Prompts",
    "notices": "Legal Notice Prompts",
    "criminal": "Criminal Law Prompts",
    "family": "Family Law Prompts",
    "consumer": "Consumer Law Prompts",
    "property": "Property & Civil Law Prompts",
    "banking": "Banking & DRT Prompts",
    "review": "Draft Review & Quality Check Prompts",
}

FIRM_HEADER = """D&D LAW ASSOCIATES
Advocates: DEEPAK ARAVIND.K | DEEPTHI.G
Door No. 49-20-5/c, Lalithanagar, R.K. Nagar, Opp Roshni Residency, Visakhapatnam-16, AP
Email: dndlawassociates@gmail.com | Mobile: 7382398999"""

PROMPTS = {
    # ──────────────────────────────────────────────
    # LEGAL DRAFTING PROMPTS
    # ──────────────────────────────────────────────
    "draft_plaint": {
        "category": "drafting",
        "title": "Draft a Plaint (Civil Suit)",
        "description": "Complete plaint with cause title, jurisdiction, facts, cause of action, limitation, schedule property, prayer, verification, and affidavit.",
        "prompt": """You are a 40-year senior advocate drafting a plaint for filing in AP courts. Follow these MANDATORY rules:

**COURT:** {court_name}
**PARTIES:**
- Plaintiff: {plaintiff_details}
- Defendant: {defendant_details}

**CASE FACTS:** {case_facts}

**DRAFTING RULES (NON-NEGOTIABLE):**
1. Cause title format: O.S. No. _____ of 2026 — IN THE COURT OF {court_designation}
2. ZERO case law in the plaint body — facts only, no citations
3. Jurisdiction paragraph: territorial + pecuniary + subject matter
4. Cause of action: specific dates, places, triggering events
5. Limitation: state the applicable article of Limitation Act
6. Valuation: suit value for court fee and jurisdiction purposes
7. Schedule property (if applicable): 4 boundaries (East/West/North/South) + survey number + admeasurement
8. ALL monetary amounts in Indian format: Rs.X,XX,XXX/- (Rupees _____ only) — Lakhs/Crores ONLY
9. Prayer clause: specific reliefs sought (a), (b), (c)... + costs + "such other relief"
10. Verification: split Personal Knowledge paragraphs from Information & Belief paragraphs
11. Supporting affidavit: MANDATORY for AP court filings
12. Document list: numbered Annexures (NOT Exhibits — Exhibits marked at trial)
13. Numbered paragraphs — consecutive, no restarting mid-document
14. Format: Arial 13pt, 1.5 line spacing, formal legal English
15. NO letterhead on court pleadings — letterhead is ONLY for notices""",
        "variables": ["court_name", "court_designation", "plaintiff_details", "defendant_details", "case_facts"]
    },

    "draft_written_statement": {
        "category": "drafting",
        "title": "Draft a Written Statement (Defence)",
        "description": "Complete written statement with preliminary objections, para-wise reply, additional defence, counter-claim, and verification.",
        "prompt": """You are a 40-year senior advocate drafting a written statement in defence. Follow these MANDATORY rules:

**COURT:** {court_name}
**SUIT:** O.S. No. {suit_number} of {year}
**DEFENDANT:** {defendant_details}
**PLAINTIFF'S CLAIMS:** {plaintiff_claims}
**DEFENCE FACTS:** {defence_facts}

**STRUCTURE (MANDATORY):**
1. CAUSE TITLE — Mirror the plaint's cause title (Plaintiff vs Defendant)
2. PRELIMINARY OBJECTIONS — Jurisdiction, limitation, maintainability, misjoinder, non-joinder, cause of action
3. PARA-WISE REPLY — Address EVERY paragraph of the plaint (admit/deny/not within knowledge)
4. ADDITIONAL DEFENCE — Counter-facts, affirmative defences
5. COUNTER-CLAIM (if applicable) — Under Order 8 Rule 6A CPC
6. PRAYER — Dismiss suit with costs, allow counter-claim
7. VERIFICATION — Personal Knowledge vs Information & Belief
8. AFFIDAVIT — Mandatory for AP courts

**RULES:**
- ZERO case law in the written statement
- Address every para of the plaint — do NOT skip any
- Use "denied as false" / "admitted" / "not within the knowledge of the defendant"
- All amounts in Indian legal format (Lakhs/Crores)
- Consecutive paragraph numbering""",
        "variables": ["court_name", "suit_number", "year", "defendant_details", "plaintiff_claims", "defence_facts"]
    },

    "draft_bail_application": {
        "category": "criminal",
        "title": "Draft Bail Application",
        "description": "Regular or anticipatory bail under BNSS with grounds, case law, and prayer.",
        "prompt": """You are a 40-year senior criminal advocate drafting a bail application under BNSS.

**BAIL TYPE:** {bail_type} (Regular Bail u/s 479/480 BNSS OR Anticipatory Bail u/s 482 BNSS)
**COURT:** {court_name}
**ACCUSED:** {accused_details}
**FIR/CRIME NO:** {fir_details}
**SECTIONS CHARGED:** {sections}
**FACTS:** {case_facts}

**STRUCTURE:**
1. CAUSE TITLE — Crl.M.P. No. _____ of 2026 / CC No. or Crime No.
2. SYNOPSIS — Brief facts + reason for bail
3. GROUNDS FOR BAIL:
   - No flight risk, roots in community
   - Cooperating with investigation
   - No tampering with evidence/witnesses
   - Severity of punishment proportionate
   - Personal liberty under Article 21
   - "Bail is rule, jail is exception" — default bail rights
   - Parity with co-accused (if applicable)
   - Medical/humanitarian grounds (if applicable)
4. CASE LAW (PERMITTED in bail applications):
   - Arnesh Kumar vs State of Bihar (arrest guidelines)
   - Sanjay Chandra vs CBI (economic offences, bail factors)
   - Satender Kumar Antil vs CBI (bail guidelines)
   - P. Chidambaram vs Directorate of Enforcement (anticipatory bail)
5. PRAYER — Grant bail with conditions
6. AFFIDAVIT — Mandatory
7. VAKALATNAMA reference

**Note for NDPS cases:** Twin conditions of Section 37 NDPS must be addressed""",
        "variables": ["bail_type", "court_name", "accused_details", "fir_details", "sections", "case_facts"]
    },

    "draft_legal_notice": {
        "category": "notices",
        "title": "Draft Legal Notice",
        "description": "Legal notice with D&D Law Associates letterhead, facts, demands, and timeline.",
        "prompt": """You are a 40-year senior advocate drafting a legal notice on D&D Law Associates letterhead.

**FROM (Client):** {client_details}
**TO (Opposite Party):** {opposite_party}
**SUBJECT:** {subject}
**FACTS:** {case_facts}
**DEMAND/RELIEF:** {demand}

**FORMAT (MANDATORY):**
1. D&D LAW ASSOCIATES LETTERHEAD:
   D&D LAW ASSOCIATES
   Advocates: DEEPAK ARAVIND.K | DEEPTHI.G
   Door No. 49-20-5/c, Lalithanagar, R.K. Nagar, Opp Roshni Residency, Visakhapatnam-16, AP
   Email: dndlawassociates@gmail.com | Mobile: 7382398999

2. Date, Reference Number
3. NOTICE UNDER {applicable_section} — specify the statute
4. Addressee details (name, address, designation)
5. Body:
   - Opening: "Under instructions from our client..."
   - Facts: chronological, specific dates, amounts
   - Legal basis: applicable sections and statutes
   - Demand: clear, specific, time-bound
   - Consequence: "failing which... compelled to initiate legal proceedings"
6. Timeline: typically 15 days for response (30 days for cheque bounce)
7. Copies: "A copy of this notice is retained for our records"
8. Signature block: Advocate name + Bar Council enrollment

**RULES:**
- ALL amounts in Indian format (Lakhs/Crores)
- Formal legal English, no emotional language
- Specific statutory basis for each demand
- Include instruction to respond to D&D office address""",
        "variables": ["client_details", "opposite_party", "subject", "case_facts", "demand", "applicable_section"]
    },

    "draft_reply_notice": {
        "category": "notices",
        "title": "Draft Reply to Legal Notice",
        "description": "Point-by-point reply to a received legal notice with D&D letterhead.",
        "prompt": """You are a 40-year senior advocate drafting a reply to a legal notice on D&D Law Associates letterhead.

**CLIENT (Noticee):** {client_details}
**NOTICE FROM:** {sender_details}
**NOTICE DATE:** {notice_date}
**NOTICE CLAIMS:** {notice_claims}
**CLIENT'S VERSION:** {client_version}

**FORMAT:**
1. D&D LAW ASSOCIATES LETTERHEAD (same as above)
2. "REPLY TO LEGAL NOTICE DATED {notice_date}"
3. Opening: "Under instructions from our client... in reply to your notice..."
4. Point-by-point reply to each claim:
   - Admitted facts
   - Denied facts (with reasons)
   - Counter-facts
5. Legal position of the client
6. Counter-demand or denial of liability
7. Warning against vexatious litigation
8. "Our client reserves all rights under law"

**RULES:**
- Address EVERY point in the original notice
- Do not make admissions that weaken client's case
- Firm but professional tone
- Keep response factual, not emotional""",
        "variables": ["client_details", "sender_details", "notice_date", "notice_claims", "client_version"]
    },

    "draft_consumer_complaint": {
        "category": "consumer",
        "title": "Draft Consumer Complaint (CPA 2019)",
        "description": "Consumer complaint under Consumer Protection Act 2019 with deficiency/defect particulars.",
        "prompt": """You are a 40-year senior advocate drafting a consumer complaint under CPA 2019.

**FORUM:** {forum_name}
**COMPLAINANT:** {complainant_details}
**OPPOSITE PARTY:** {opposite_party}
**PRODUCT/SERVICE:** {product_service}
**DEFECT/DEFICIENCY:** {defect_deficiency}
**CLAIM VALUE:** {claim_value}

**STRUCTURE:**
1. CAUSE TITLE — C.C. No. _____ of 2026 (Consumer uses "Complainant" and "Opposite Party")
2. PARTIES — Complainant address, OP registered office + branch
3. FACTS — Chronological purchase/service, defect/deficiency discovery
4. DEFICIENCY OF SERVICE / DEFECT IN GOODS — Specific particulars
5. UNFAIR TRADE PRACTICE (if applicable) — Section 2(47) CPA 2019
6. CAUSE OF ACTION — When and how the right to complain arose
7. JURISDICTION — Territorial + Pecuniary (District/State/National)
8. LIMITATION — 2 years from cause of action (Section 36 CPA 2019)
9. PRAYER — Replacement/refund/compensation/costs
10. VERIFICATION
11. AFFIDAVIT
12. DOCUMENT LIST

**RULES:**
- ZERO case law in complaint body
- Consumer-specific terminology: Complainant, Opposite Party, deficiency, defect
- Product liability provisions if against manufacturer (Section 69)
- All amounts in Indian legal format""",
        "variables": ["forum_name", "complainant_details", "opposite_party", "product_service", "defect_deficiency", "claim_value"]
    },

    "draft_divorce_petition": {
        "category": "family",
        "title": "Draft Divorce Petition (HMA/SMA)",
        "description": "Divorce petition under Section 13 HMA or mutual consent under Section 13-B.",
        "prompt": """You are a 40-year senior family law advocate drafting a divorce petition.

**COURT:** Family Court, {location}
**PETITION TYPE:** {petition_type} (Contested u/s 13 HMA OR Mutual Consent u/s 13-B HMA)
**PETITIONER:** {petitioner_details}
**RESPONDENT:** {respondent_details}
**MARRIAGE DETAILS:** {marriage_details}
**GROUNDS:** {grounds}
**CHILDREN:** {children_details}

**STRUCTURE:**
1. CAUSE TITLE — O.P. No. _____ of 2026 — IN THE FAMILY COURT AT {location}
2. PARTIES — Full names, father's name, age, occupation, address
3. MARRIAGE PARTICULARS — Date, place, rites, registration
4. FACTS — Chronological account of matrimonial breakdown
5. GROUNDS FOR DIVORCE — Section 13(1)(ia) cruelty / (ib) desertion / (ii) conversion / etc.
6. MUTUAL CONSENT (if 13-B) — Terms: custody, maintenance, property, stridhan
7. CUSTODY & MAINTENANCE — Welfare of child paramount, Section 26 HMA
8. PRAYER — Dissolution of marriage, custody, maintenance, costs
9. VERIFICATION — Personal knowledge
10. AFFIDAVIT — Mandatory

**RULES:**
- ZERO case law in petition body
- No limitation for matrimonial relief
- Territorial jurisdiction: where parties last resided together OR where wife currently resides
- Sensitive handling of domestic violence facts if applicable""",
        "variables": ["location", "petition_type", "petitioner_details", "respondent_details", "marriage_details", "grounds", "children_details"]
    },

    "draft_cheque_bounce_complaint": {
        "category": "criminal",
        "title": "Draft Cheque Bounce Complaint (Section 138 NI Act)",
        "description": "Criminal complaint for dishonour of cheque with full timeline checklist.",
        "prompt": """You are a 40-year senior advocate drafting a Section 138 NI Act complaint.

**COURT:** Court of Judicial Magistrate First Class, {location}
**COMPLAINANT:** {complainant_details}
**ACCUSED:** {accused_details}
**CHEQUE DETAILS:** {cheque_details}
**UNDERLYING DEBT:** {debt_details}

**MANDATORY TIMELINE CHECKLIST:**
1. Date of cheque: ___
2. Date presented to bank: ___ (within validity period)
3. Date of return memo (dishonour): ___
4. Date of legal notice (within 30 days of return memo): ___
5. Date notice served/received by drawer: ___
6. 15-day notice period expired: ___
7. Date of filing complaint (within 30 days of notice period expiry): ___

**STRUCTURE:**
1. CAUSE TITLE — C.C. No. _____ of 2026
2. PARTIES — Complainant (payee/holder) vs Accused (drawer)
3. FACTS — Legally enforceable debt, cheque issued, presented, dishonoured
4. NOTICE — Legal notice sent within 30 days, served, 15 days expired, no payment
5. SECTION 139 PRESUMPTION — Statutory presumption of legally enforceable debt
6. PRAYER — Conviction, imprisonment (up to 2 years), compensation (twice the cheque amount)
7. EVIDENCE ON AFFIDAVIT — Section 145 NI Act
8. DOCUMENT LIST — Cheque, return memo, legal notice, postal receipts, AD card

**RULES:**
- Case law PERMITTED in 138 complaints (unlike plaints)
- Territorial jurisdiction: where cheque was delivered for collection (Dashrath Rupsingh Rathod)
- All amounts in Indian format
- Ensure EVERY date in the timeline is verified""",
        "variables": ["location", "complainant_details", "accused_details", "cheque_details", "debt_details"]
    },

    "draft_writ_petition": {
        "category": "drafting",
        "title": "Draft Writ Petition (Article 226)",
        "description": "Writ petition before High Court — Mandamus, Certiorari, Prohibition, Habeas Corpus, Quo Warranto.",
        "prompt": """You are a 40-year senior constitutional advocate drafting a writ petition under Article 226.

**HIGH COURT:** {high_court}
**WRIT TYPE:** {writ_type} (Mandamus/Certiorari/Prohibition/Habeas Corpus/Quo Warranto)
**PETITIONER:** {petitioner_details}
**RESPONDENT:** {respondent_details}
**FACTS:** {case_facts}
**RELIEF SOUGHT:** {relief}

**STRUCTURE:**
1. CAUSE TITLE — W.P. No. _____ of 2026 — IN THE HIGH COURT OF {high_court}
2. SYNOPSIS AND LIST OF DATES — Chronological timeline of events
3. PARTIES — Petitioner, Respondent (State/Authority/Official)
4. FACTS — Detailed factual narrative
5. GROUNDS — Constitutional violations, fundamental rights, illegality, irrationality, procedural impropriety
6. CASE LAW (PERMITTED in writ petitions):
   - Wednesbury reasonableness
   - Natural justice violations
   - Article 14/19/21 violations
7. PRAYER — Issue writ of {writ_type}, quash order, direct compliance
8. INTERIM PRAYER — Stay of impugned order pending disposal
9. AFFIDAVIT
10. DOCUMENT LIST

**Note:** No limitation for writs but laches/delay can be fatal. Explain delay if any.""",
        "variables": ["high_court", "writ_type", "petitioner_details", "respondent_details", "case_facts", "relief"]
    },

    "draft_ia_application": {
        "category": "drafting",
        "title": "Draft Interlocutory Application (IA)",
        "description": "IA for interim injunction, stay, amendment, addition of party, etc.",
        "prompt": """You are a 40-year senior advocate drafting an Interlocutory Application.

**COURT:** {court_name}
**MAIN SUIT:** O.S. No. {suit_number} of {year}
**IA TYPE:** {ia_type} (Interim Injunction u/O.39 R.1&2 / Stay / Amendment / Addition of Party / Appointment of Commissioner / Receiver)
**APPLICANT:** {applicant_details}
**RESPONDENT:** {respondent_details}
**GROUNDS:** {grounds}

**STRUCTURE:**
1. CAUSE TITLE — I.A. No. _____ of 2026 in O.S. No. {suit_number} of {year}
2. PARTIES — Applicant (Plaintiff/Defendant in main suit) vs Respondent
3. FACTS — Brief reference to main suit + specific facts for IA
4. GROUNDS — Why interim relief is necessary:
   - For Injunction: Prima facie case + Balance of convenience + Irreparable injury (three-part test)
   - For Stay: Arguable case + Balance of equities
   - For Amendment: No prejudice to other side + Necessary for determination
5. URGENCY — Why the application needs immediate hearing
6. PRAYER — Specific interim relief sought
7. AFFIDAVIT — Mandatory

**RULES:**
- Brief and focused — IAs should not replicate the entire plaint
- Case law PERMITTED in IAs
- Court fee for IA: Rs.100-200 (verify with court_fee_calculator)""",
        "variables": ["court_name", "suit_number", "year", "ia_type", "applicant_details", "respondent_details", "grounds"]
    },

    "draft_appeal": {
        "category": "drafting",
        "title": "Draft Appeal (Civil/Criminal)",
        "description": "First appeal, second appeal, criminal appeal, or revision petition.",
        "prompt": """You are a 40-year senior appellate advocate drafting an appeal.

**COURT:** {appellate_court}
**APPEAL TYPE:** {appeal_type} (First Appeal u/s 96 CPC / Second Appeal u/s 100 CPC / Criminal Appeal / Revision u/s 115 CPC)
**IMPUGNED ORDER:** {order_details}
**APPELLANT:** {appellant_details}
**RESPONDENT:** {respondent_details}
**GROUNDS OF APPEAL:** {grounds}

**STRUCTURE:**
1. CAUSE TITLE — A.S. No. _____ / Crl.A. No. _____ of 2026
2. IMPUGNED JUDGMENT — Court, date, case number, summary of findings
3. BRIEF FACTS — Concise narrative from trial record
4. GROUNDS OF APPEAL — Numbered, each a substantial point:
   - Error of law / fact / mixed question
   - Perverse findings not supported by evidence
   - Non-consideration of material evidence
   - Violation of natural justice
   - Substantial question of law (for second appeals)
5. CASE LAW (PERMITTED — essential in appeals)
6. PRAYER — Set aside/modify impugned order, remand/allow appeal
7. INTERIM PRAYER — Stay of execution pending appeal
8. AFFIDAVIT

**LIMITATION:**
- First appeal: 90 days from decree
- Criminal appeal: 30 days from sentence
- Revision: 90 days from order""",
        "variables": ["appellate_court", "appeal_type", "order_details", "appellant_details", "respondent_details", "grounds"]
    },

    "draft_partition_suit": {
        "category": "property",
        "title": "Draft Partition Suit",
        "description": "Partition suit with pedigree table, share calculation, and schedule property.",
        "prompt": """You are a 40-year senior property law advocate drafting a partition suit.

**COURT:** {court_name}
**PLAINTIFF:** {plaintiff_details}
**DEFENDANTS:** {defendant_details}
**FAMILY DETAILS:** {family_tree}
**PROPERTIES:** {properties}

**STRUCTURE:**
1. CAUSE TITLE — O.S. No. _____ of 2026
2. PEDIGREE TABLE — Family tree showing all coparceners/legal heirs
3. SHARE CALCULATION:
   - Hindu Succession Act 1956 + 2005 Amendment (daughters = sons in coparcenary)
   - Class I heirs under Section 8
   - Per stirpes vs per capita distribution
4. SCHEDULE PROPERTY — For each property:
   - Description + location + survey number
   - 4 boundaries: East, West, North, South
   - Admeasurement (area in sq.yards/acres)
   - Present possession
   - Approximate market value
5. FACTS — Joint family property, how acquired, present possession
6. CAUSE OF ACTION — Refusal to partition, exclusion from property
7. PRAYER — Preliminary decree declaring shares + Final decree for partition by metes and bounds
8. COURT FEE — On plaintiff's share value
9. VERIFICATION + AFFIDAVIT

**RULES:**
- No limitation for coparcener's partition (right subsists till partition)
- If ouster alleged — 12 years limitation
- All property values in Indian format""",
        "variables": ["court_name", "plaintiff_details", "defendant_details", "family_tree", "properties"]
    },

    "draft_execution_petition": {
        "category": "drafting",
        "title": "Draft Execution Petition (Order 21 CPC)",
        "description": "Execution of decree — money, possession, specific performance.",
        "prompt": """You are a 40-year senior advocate drafting an Execution Petition under Order 21 CPC.

**COURT:** {court_name}
**DECREE:** {decree_details} (Court, case number, date of decree)
**DECREE HOLDER:** {dh_details}
**JUDGMENT DEBTOR:** {jd_details}
**RELIEF IN DECREE:** {relief}
**AMOUNT DUE:** {amount_due}

**STRUCTURE:**
1. CAUSE TITLE — E.P. No. _____ of 2026 in O.S. No. _____ of ____
2. DECREE DETAILS — Court, date, operative portion
3. NON-COMPLIANCE — Judgment debtor's failure to comply
4. MODE OF EXECUTION:
   - Money decree: Attachment + sale of property / arrest of JD
   - Possession decree: Delivery of possession by court bailiff
   - Specific performance: Enforce specific acts
5. PROPERTY TO BE ATTACHED (if money decree):
   - Immovable property details
   - Movable property / bank accounts
6. PRAYER — Execute decree, attach and sell property, deliver possession
7. AFFIDAVIT

**LIMITATION:** 12 years from date of decree or last order on execution""",
        "variables": ["court_name", "decree_details", "dh_details", "jd_details", "relief", "amount_due"]
    },

    "draft_mact_claim": {
        "category": "drafting",
        "title": "Draft MACT Claim (Motor Accident)",
        "description": "Motor Accident Compensation claim under Section 166 MV Act.",
        "prompt": """You are a 40-year senior advocate drafting a MACT claim under Section 166 MV Act.

**TRIBUNAL:** Motor Accident Claims Tribunal, {location}
**CLAIMANT:** {claimant_details}
**RESPONDENTS:** {respondent_details} (Driver, Owner, Insurance Company)
**ACCIDENT DETAILS:** {accident_details}
**INJURIES/DEATH:** {injury_details}
**CLAIM AMOUNT:** {claim_amount}

**STRUCTURE:**
1. CAUSE TITLE — MACP No. _____ of 2026
2. PARTIES — Claimant, Respondent 1 (Driver), R2 (Owner), R3 (Insurance Co.)
3. ACCIDENT DETAILS — Date, time, place, vehicle numbers, FIR/MLC
4. NEGLIGENCE — Rash and negligent driving particulars
5. INJURIES/DEATH — Medical records, disability percentage, treatment expenses
6. COMPENSATION HEADS (Sarla Verma + Pranay Sethi methodology):
   - Loss of earning capacity (multiplier method)
   - Medical expenses (past + future)
   - Loss of amenities of life
   - Pain and suffering
   - Future loss of earnings (if disability)
   - Funeral expenses (if death)
   - Loss of estate (if death)
   - Loss of consortium (if death)
   - Conventional additions (Pranay Sethi — Rs.15,000-70,000 per head)
7. TOTAL CLAIM — Itemized + aggregate
8. PRAYER — Compensation with 9% interest from accident date
9. AFFIDAVIT + DOCUMENT LIST

**LIMITATION:** 6 months from accident (liberally condonable — Section 166(3))
**JURISDICTION:** MACT at place where accident occurred (exclusive — bar on civil court)""",
        "variables": ["location", "claimant_details", "respondent_details", "accident_details", "injury_details", "claim_amount"]
    },

    # ──────────────────────────────────────────────
    # LEGAL RESEARCH PROMPTS
    # ──────────────────────────────────────────────
    "research_case_law": {
        "category": "research",
        "title": "Case Law Research",
        "description": "Find and analyze relevant case law on a specific legal issue.",
        "prompt": """You are a 40-year senior advocate conducting case law research.

**LEGAL ISSUE:** {legal_issue}
**JURISDICTION:** {jurisdiction}
**APPLICABLE STATUTE:** {statute}
**CONTEXT:** {context}

**RESEARCH METHODOLOGY:**
1. Identify the core legal question
2. Search for:
   - Supreme Court decisions (binding on all courts)
   - High Court decisions (persuasive/binding within jurisdiction)
   - Recent decisions (last 5 years — evolving law)
   - Landmark decisions (Menaka Gandhi, Vishaka, etc.)
3. For each case found, provide:
   - Full citation: Party1 vs Party2 (Year) Reporter Page
   - Court and bench strength
   - Facts (brief)
   - Ratio decidendi (the binding principle)
   - How it applies to the current case
4. Distinguish unfavorable cases — explain why they don't apply
5. Identify any conflicting judgments across High Courts
6. Note if the issue is pending before a larger bench

**SOURCES:** Indian Kanoon, SCC Online, Manupatra, LiveLaw, Bar & Bench

**OUTPUT:** Structured research memo with citations and analysis""",
        "variables": ["legal_issue", "jurisdiction", "statute", "context"]
    },

    "research_statute": {
        "category": "research",
        "title": "Statute Analysis & Interpretation",
        "description": "Deep analysis of statutory provisions with amendments and judicial interpretation.",
        "prompt": """You are a 40-year senior advocate analyzing a statutory provision.

**STATUTE:** {statute_name}
**SECTION:** {section}
**ISSUE:** {issue}

**ANALYSIS FRAMEWORK:**
1. TEXT — Exact text of the provision (from bare act)
2. AMENDMENTS — Any amendments since enactment, especially:
   - BNS/BNSS/BSA replacements (2023)
   - Recent amendments (2019-2026)
3. JUDICIAL INTERPRETATION — How courts have interpreted this section
4. SCOPE & APPLICATION — What falls within and outside the section
5. EXCEPTIONS — Proviso, exemptions, carve-outs
6. PROCEDURE — How to invoke this section (application/complaint/suit)
7. LIMITATION — Time limit for invoking this section
8. INTERPLAY — How this section interacts with other statutes
9. PRACTICAL ADVICE — How to use this section in the current case

**IPC→BNS / CrPC→BNSS MAPPING:** If the section is from old law, provide the new law equivalent.""",
        "variables": ["statute_name", "section", "issue"]
    },

    "research_opposing_arguments": {
        "category": "research",
        "title": "Anticipate Opposing Arguments",
        "description": "Research and prepare counter-arguments to opposing counsel's likely positions.",
        "prompt": """You are a 40-year senior advocate anticipating opposing counsel's arguments.

**OUR CASE:** {our_case}
**OUR POSITION:** {our_position}
**OPPOSING PARTY'S LIKELY STANCE:** {opposing_stance}

**ANALYSIS:**
1. LIST all possible arguments opposing counsel can raise:
   - Jurisdictional objections
   - Limitation defences
   - Factual denials
   - Legal defences (statutory, equitable)
   - Procedural objections
2. For each opposing argument:
   - The argument in their strongest form (steelman it)
   - Case law they might cite
   - Our counter-argument
   - Case law supporting our counter
   - Weaknesses in their position
3. STRATEGY:
   - Which arguments are their strongest?
   - Where are they vulnerable?
   - Pre-emptive measures we should take in our pleading
   - Evidence we need to gather to counter them""",
        "variables": ["our_case", "our_position", "opposing_stance"]
    },

    # ──────────────────────────────────────────────
    # CASE ANALYSIS PROMPTS
    # ──────────────────────────────────────────────
    "analyze_case_strength": {
        "category": "analysis",
        "title": "Case Strength Assessment",
        "description": "Evaluate case strength with strategic advice on best approach.",
        "prompt": """You are a 40-year senior advocate assessing case strength.

**CASE FACTS:** {case_facts}
**CLIENT'S POSITION:** {client_position}
**RELIEF SOUGHT:** {relief_sought}
**OPPOSING FACTS:** {opposing_facts}

**ASSESSMENT FRAMEWORK:**
1. STRENGTH RATING: Strong / Moderate / Weak (with reasons)
2. STRONGEST POINTS — What works in our favor
3. WEAKEST POINTS — Where we are vulnerable
4. EVIDENCE ANALYSIS — What evidence we have, what we need
5. FORUM SELECTION — Best court/tribunal for this matter:
   - Civil court vs specialized tribunal (DRT/Consumer/MACT/RERA/NCLT)
   - Family Court vs criminal court for matrimonial matters
   - Pecuniary jurisdiction — which level of court
6. RELIEF STRATEGY — Best combination of reliefs to pray for
7. INTERIM RELIEF — Do we need urgent interim orders?
8. LIMITATION — Is the case within time? If borderline, explain options
9. SETTLEMENT POTENTIAL — Is ADR (mediation/arbitration) advisable?
10. RISKS & COSTS — Litigation costs, time estimate, risk of adverse order
11. RECOMMENDED APPROACH — Step-by-step action plan

**Be brutally honest.** If the case is weak, say so. Better to advise settlement than waste resources on a losing case.""",
        "variables": ["case_facts", "client_position", "relief_sought", "opposing_facts"]
    },

    "analyze_judgment": {
        "category": "analysis",
        "title": "Analyze a Court Judgment",
        "description": "Deep analysis of a judgment — ratio, obiter, applicability, appeal potential.",
        "prompt": """You are a 40-year senior advocate analyzing a court judgment.

**JUDGMENT:** {judgment_text_or_citation}
**CONTEXT:** {context}
**PURPOSE:** {purpose} (Appeal? Distinguish? Apply?)

**ANALYSIS:**
1. PARTIES & COURT — Who, which court, which bench
2. FACTS — Key facts of the case
3. ISSUES FRAMED — Legal questions decided
4. RATIO DECIDENDI — The binding legal principle
5. OBITER DICTA — Observations not binding but persuasive
6. REASONING — How the court reached its conclusion
7. DISTINGUISHING FACTORS — How this case differs from ours
8. APPLICABILITY — Can we use this judgment? How?
9. APPEAL POTENTIAL — If adverse:
   - Grounds for appeal
   - Substantial question of law (for second appeal)
   - Chances of reversal
   - Stay application strategy
10. CITATIONS WITHIN — Other important cases cited in this judgment""",
        "variables": ["judgment_text_or_citation", "context", "purpose"]
    },

    "analyze_contract": {
        "category": "analysis",
        "title": "Contract Review & Risk Analysis",
        "description": "Review a contract for risks, missing clauses, and enforceability issues.",
        "prompt": """You are a 40-year senior advocate reviewing a contract.

**CONTRACT TYPE:** {contract_type}
**PARTIES:** {parties}
**KEY TERMS:** {key_terms}
**CLIENT'S CONCERNS:** {concerns}

**REVIEW CHECKLIST:**
1. VALIDITY — Offer, acceptance, consideration, capacity, free consent (Sections 10-23 Contract Act)
2. ESSENTIAL TERMS — Completeness, certainty, definiteness
3. RISK CLAUSES:
   - Indemnity (Section 124-125) — Who bears risk?
   - Limitation of liability — Unreasonable caps?
   - Force majeure — Adequately defined?
   - Termination — Unilateral? Notice period? Consequences?
   - Penalty vs liquidated damages (Section 74 — Fateh Chand principle)
4. MISSING CLAUSES — What should be added?
5. ONE-SIDED TERMS — Unconscionable provisions?
6. GOVERNING LAW & JURISDICTION — Appropriate?
7. DISPUTE RESOLUTION — Arbitration clause? Institutional?
8. STAMP DUTY & REGISTRATION — Required?
9. ENFORCEABILITY — Any provisions unenforceable?
10. RECOMMENDATIONS — Specific amendments to protect client""",
        "variables": ["contract_type", "parties", "key_terms", "concerns"]
    },

    # ──────────────────────────────────────────────
    # SPECIALIZED PROMPTS
    # ──────────────────────────────────────────────
    "draft_drt_application": {
        "category": "banking",
        "title": "Draft DRT Original Application",
        "description": "OA for recovery of debt under RDDBFI Act / SARFAESI challenge.",
        "prompt": """You are a 40-year senior banking law advocate drafting a DRT application.

**APPLICATION TYPE:** {app_type} (OA for Recovery / SA under Section 17 SARFAESI / Appeal to DRAT)
**TRIBUNAL:** {tribunal}
**APPLICANT:** {applicant_details}
**RESPONDENT:** {respondent_details}
**DEBT/CLAIM:** {debt_details}
**SECURITY:** {security_details}

**STRUCTURE:**
1. CAUSE TITLE — O.A. No. _____ of 2026 / S.A. No. _____ of 2026
2. PARTIES — Bank/Financial Institution vs Borrower/Guarantor
3. LOAN DETAILS — Facility, sanction, disbursement, terms
4. DEFAULT — NPA date, amount outstanding
5. NOTICES — Section 13(2) SARFAESI notice (60 days) / DRT notice
6. PRAYER — Recovery certificate / Set aside SARFAESI action
7. INTERIM PRAYER — Attachment before judgment / Stay of auction

**DRT PECUNIARY:** Rs.10 Lakh+ (bar on civil court for covered debts)
**LIMITATION:** 3 years from NPA date / 45 days for SARFAESI challenge""",
        "variables": ["app_type", "tribunal", "applicant_details", "respondent_details", "debt_details", "security_details"]
    },

    "draft_rera_complaint": {
        "category": "consumer",
        "title": "Draft RERA Complaint",
        "description": "Complaint to RERA Authority against builder/promoter.",
        "prompt": """You are a 40-year senior advocate drafting a RERA complaint.

**AUTHORITY:** AP-RERA / {authority}
**COMPLAINANT:** {complainant_details}
**PROMOTER/BUILDER:** {promoter_details}
**PROJECT:** {project_details}
**GRIEVANCE:** {grievance}
**CLAIM:** {claim_amount}

**STRUCTURE:**
1. COMPLAINT under Section 31 RERA Act 2016
2. COMPLAINANT — Allottee/buyer details, agreement date
3. PROMOTER — Registration number, project details
4. AGREEMENT TERMS — Possession date, payment schedule, specifications
5. BREACH — Delay, defect, deviation from plan, non-registration
6. SECTIONS ATTRACTED — 11(4), 14, 18 RERA Act
7. PRAYER — Refund with interest / Possession / Compensation
8. AFFIDAVIT + DOCUMENTS

**LIMITATION:** 3 years or 1 year from possession (whichever earlier)
**JURISDICTION:** RERA exclusive — bar on civil court (Section 79)""",
        "variables": ["authority", "complainant_details", "promoter_details", "project_details", "grievance", "claim_amount"]
    },

    "draft_quash_petition": {
        "category": "criminal",
        "title": "Draft Quash Petition (Section 528 BNSS)",
        "description": "High Court petition to quash FIR/charge sheet/criminal proceedings.",
        "prompt": """You are a 40-year senior advocate drafting a quash petition under Section 528 BNSS (old CrPC 482).

**HIGH COURT:** {high_court}
**PETITIONER:** {petitioner_details}
**RESPONDENT:** State / {complainant}
**FIR/CASE:** {case_details}
**SECTIONS CHARGED:** {sections}
**GROUNDS FOR QUASHING:** {grounds}

**STRUCTURE:**
1. CAUSE TITLE — Crl.P. No. _____ of 2026 (Under Section 528 BNSS)
2. SYNOPSIS AND LIST OF DATES
3. FACTS — FIR/complaint, chargesheet, proceedings
4. GROUNDS (Case law MANDATORY):
   - No offence made out from FIR/complaint (Bhajan Lal categories)
   - Abuse of process / ulterior motive
   - Civil dispute given criminal color
   - Matrimonial settlement (if 498A/DV)
   - Compounded/compoundable offence
5. CASE LAW (ESSENTIAL):
   - State of Haryana vs Bhajan Lal (7 categories for quashing)
   - R.P. Kapur vs State of Punjab
   - Gian Singh vs State of Punjab (settlement in compoundable offences)
   - Arnesh Kumar vs State of Bihar (if arrest challenged)
6. PRAYER — Quash FIR/proceedings, stay arrest pending hearing
7. INTERIM PRAYER — Stay of further proceedings / arrest

**Note:** High Court can exercise inherent power — no limitation""",
        "variables": ["high_court", "petitioner_details", "complainant", "case_details", "sections", "grounds"]
    },

    # ──────────────────────────────────────────────
    # REVIEW PROMPTS
    # ──────────────────────────────────────────────
    "review_draft": {
        "category": "review",
        "title": "Review & Improve a Legal Draft",
        "description": "Senior advocate review of any legal document for errors, weaknesses, and improvements.",
        "prompt": """You are a 40-year senior advocate reviewing a legal draft for quality.

**DOCUMENT TYPE:** {document_type}
**DRAFT:** {draft_text}

**10-POINT SENIOR ADVOCATE SCRUTINY:**
1. JURISDICTIONAL PRECISION — Territorial + pecuniary + subject-matter verified?
2. LIMITATION VIGILANCE — Correct article, within time?
3. PLEADING PURITY — No case law in pleadings? (Permitted only in applications/appeals)
4. CAUSE OF ACTION — Specific dates, places, events stated?
5. SCHEDULE PROPERTY — 4 boundaries, survey number, admeasurement?
6. MONETARY AMOUNTS — All in Indian format (Lakhs/Crores)?
7. AFFIDAVIT — Included for AP court filing?
8. VERIFICATION — Personal Knowledge vs Information & Belief split?
9. NO ASSUMPTIONS — All facts verified with client?
10. PROFESSIONAL LANGUAGE — Formal legal English? Proper honorifics?

**ADDITIONAL CHECKS:**
- Are the correct statutes cited? (BNS not IPC, BNSS not CrPC)
- Is the cause title format correct for this court?
- Are paragraphs consecutively numbered?
- Is the prayer complete and specific?
- Any procedural requirements missed?

**OUTPUT:**
- List of errors found (critical and minor)
- Suggested improvements
- Missing elements that should be added
- Overall assessment: Ready / Needs Revision / Major Rewrite""",
        "variables": ["document_type", "draft_text"]
    },

    "review_opponent_draft": {
        "category": "review",
        "title": "Analyze Opponent's Pleading",
        "description": "Dissect opposing party's plaint/complaint to find weaknesses for defence.",
        "prompt": """You are a 40-year senior advocate analyzing an opponent's pleading.

**DOCUMENT TYPE:** {document_type} (Plaint/Complaint/Notice)
**OPPONENT'S DOCUMENT:** {document_text}
**OUR CLIENT'S POSITION:** {our_position}

**ANALYSIS:**
1. JURISDICTIONAL ISSUES — Can we challenge jurisdiction? Wrong court? Wrong valuation?
2. LIMITATION — Is the suit/complaint time-barred? Calculate exact dates.
3. CAUSE OF ACTION — Is it properly stated? Any vagueness to exploit?
4. FACTUAL WEAKNESSES — Inconsistencies, contradictions, unsubstantiated claims
5. LEGAL WEAKNESSES — Wrong sections cited? Inapplicable law? Missing ingredients?
6. PROCEDURAL DEFECTS — Non-joinder, misjoinder, wrong format, missing affidavit
7. ADMISSIONS — Any admissions by opponent that help our case?
8. MISSING ELEMENTS — What they failed to plead that weakens their case
9. DEFENCE STRATEGY — How to structure our written statement/reply
10. PRELIMINARY OBJECTIONS — What can we raise before going to merits?

**OUTPUT:** Defence strategy memo with specific objections and counter-arguments""",
        "variables": ["document_type", "document_text", "our_position"]
    },

    # ──────────────────────────────────────────────
    # QUICK REFERENCE PROMPTS
    # ──────────────────────────────────────────────
    "quick_limitation_check": {
        "category": "analysis",
        "title": "Quick Limitation Check",
        "description": "Fast limitation period check for any type of case.",
        "prompt": """Check the limitation period for this matter:

**CASE TYPE:** {case_type}
**DATE OF CAUSE OF ACTION:** {coa_date}
**TODAY'S DATE:** {today}

Provide:
1. Applicable article of Limitation Act
2. Limitation period
3. Expiry date
4. Status: WITHIN TIME / APPROACHING / URGENT / CRITICAL / EXPIRED
5. If expired — can delay be condoned? Under which provision?
6. Any extension possible (Section 5, 6-8, 12, 14, 17, 18)?""",
        "variables": ["case_type", "coa_date", "today"]
    },

    "quick_section_lookup": {
        "category": "research",
        "title": "Quick Section Lookup",
        "description": "Instantly find the relevant section for a legal concept.",
        "prompt": """Find the exact statutory provision for:

**CONCEPT:** {concept}
**STATUTE (if known):** {statute}
**CONTEXT:** {context}

Provide:
1. Exact section number and statute
2. Key ingredients/requirements
3. If old law (IPC/CrPC/Evidence Act) — give NEW law equivalent (BNS/BNSS/BSA)
4. Procedure to invoke
5. Court/forum with jurisdiction
6. Limitation period
7. Any recent amendments""",
        "variables": ["concept", "statute", "context"]
    },

    "draft_affidavit": {
        "category": "drafting",
        "title": "Draft Affidavit",
        "description": "Supporting affidavit for any court filing (mandatory in AP/Telangana).",
        "prompt": """Draft a supporting affidavit for the following filing:

**COURT:** {court_name}
**CASE:** {case_details}
**DEPONENT:** {deponent_details}
**FILING TYPE:** {filing_type}

**FORMAT:**
1. Title: AFFIDAVIT
2. Court and case reference
3. "I, [Name], aged [age], [occupation], residing at [address], do hereby solemnly affirm and state on oath as follows:"
4. Para 1: "I am the Plaintiff/Petitioner/Applicant in the above case and as such I am competent to swear this affidavit."
5. Subsequent paras: State facts verified on oath — mirror the main petition paragraphs
6. Split: "I state the above facts are true to my knowledge" (personal knowledge paras) vs "I state the above facts are true to my information and belief" (information & belief paras)
7. "I solemnly affirm that the contents of this affidavit are true and correct to the best of my knowledge and belief and nothing material has been concealed or misstated."
8. Signature: DEPONENT
9. Verification: Place, date
10. IDENTIFIED BY: Advocate name + enrollment number

**NOTE:** This affidavit is MANDATORY for all AP/Telangana court filings.""",
        "variables": ["court_name", "case_details", "deponent_details", "filing_type"]
    },

    "draft_vakalatnama": {
        "category": "drafting",
        "title": "Draft Vakalatnama / Power of Attorney",
        "description": "Authorization for advocate to appear and plead.",
        "prompt": """Draft a Vakalatnama authorizing D&D Law Associates.

**COURT:** {court_name}
**CASE:** {case_details}
**CLIENT:** {client_details}
**ADVOCATE:** DEEPAK ARAVIND.K / DEEPTHI.G, D&D Law Associates

**FORMAT:**
VAKALATNAMA

In the {court_name}
{Case reference}

I/We, {client_name}, do hereby authorize and appoint:
1. Sri/Smt. DEEPAK ARAVIND.K, Advocate
2. Sri/Smt. DEEPTHI.G, Advocate

of D&D Law Associates, Visakhapatnam, to appear, plead, and act on my/our behalf in the above matter and in all proceedings connected therewith, including appeals, revisions, reviews, execution, and all interlocutory applications.

The said advocates are authorized to:
- File, sign, and verify all pleadings and applications
- Admit, deny, and compromise claims
- Receive notices and summons on my behalf
- Withdraw or compromise the suit/petition
- Do all acts as may be necessary for the conduct of the case

Date: _______________
Place: Visakhapatnam

Client Signature: _______________
Name: {client_name}
Address: {client_address}

Accepted:
Advocate Signature: _______________
(DEEPAK ARAVIND.K / DEEPTHI.G)
D&D Law Associates""",
        "variables": ["court_name", "case_details", "client_details", "client_name", "client_address"]
    },

    "draft_arbitration": {
        "category": "drafting",
        "title": "Draft Arbitration Application",
        "description": "Section 9/11/34/36/37 Arbitration Act applications.",
        "prompt": """You are a 40-year senior arbitration advocate drafting an application.

**APPLICATION TYPE:** {app_type} (Section 9 Interim / Section 11 Appointment / Section 34 Set Aside / Section 36 Enforcement / Section 37 Appeal)
**COURT/TRIBUNAL:** {court_name}
**APPLICANT:** {applicant_details}
**RESPONDENT:** {respondent_details}
**ARBITRATION CLAUSE:** {arb_clause}
**FACTS:** {case_facts}

**KEY PROVISIONS:**
- Section 7: Valid arbitration agreement (in writing)
- Section 8: Bar on judicial intervention (refer to arbitration)
- Section 9: Interim measures by court
- Section 11: Appointment of arbitrator by court
- Section 16: Competence-competence (tribunal decides jurisdiction)
- Section 29A: Time limit for award (12+6 months)
- Section 34: Set aside award (3 months + 30 days)
- Section 36: Enforcement of award as decree

Draft the application with proper structure, grounds, and prayer.""",
        "variables": ["app_type", "court_name", "applicant_details", "respondent_details", "arb_clause", "case_facts"]
    },

    "letter_to_client": {
        "category": "notices",
        "title": "Draft Letter to Client",
        "description": "Professional client communication on D&D letterhead.",
        "prompt": """Draft a professional letter to client on D&D Law Associates letterhead.

**CLIENT:** {client_name}
**MATTER:** {matter}
**PURPOSE:** {purpose}
**KEY POINTS:** {key_points}

**FORMAT:**
D&D LAW ASSOCIATES letterhead
Date: {date}
Ref: D&D/{ref_number}/2026

To,
{client_name}
{client_address}

Subject: {subject}

Dear {salutation},

[Body — professional, clear, actionable]

[If advice — structured as points]
[If update — chronological]
[If instructions needed — specific and clear]

With warm regards,
For D&D Law Associates

DEEPAK ARAVIND.K
Advocate
Mob: 7382398999""",
        "variables": ["client_name", "matter", "purpose", "key_points", "date", "ref_number", "client_address", "subject", "salutation"]
    },
}


def get_prompt(prompt_key: str) -> dict:
    return PROMPTS.get(prompt_key, {"error": f"Prompt '{prompt_key}' not found"})


def list_prompts(category: str = None) -> list:
    results = []
    for key, prompt in PROMPTS.items():
        if category and prompt["category"] != category:
            continue
        results.append({
            "key": key,
            "title": prompt["title"],
            "category": prompt["category"],
            "description": prompt["description"],
            "variables": prompt.get("variables", [])
        })
    return results


def get_categories() -> dict:
    return PROMPT_CATEGORIES


def fill_prompt(prompt_key: str, **kwargs) -> str:
    prompt_data = PROMPTS.get(prompt_key)
    if not prompt_data:
        return f"Error: Prompt '{prompt_key}' not found"

    text = prompt_data["prompt"]
    for var in prompt_data.get("variables", []):
        placeholder = "{" + var + "}"
        value = kwargs.get(var, f"[{var.upper().replace('_', ' ')}]")
        text = text.replace(placeholder, str(value))
    return text
