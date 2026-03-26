"""
Drafter & Researcher — D&D Law Associates
AI-Powered Legal Drafting & Research Platform
Run: python3.11 -m streamlit run app.py
"""

import streamlit as st
from datetime import datetime, date

# Core modules
from core.amount_converter import amount_to_legal_format
from core.limitation_calculator import (
    calculate_limitation, find_articles, list_all_articles, LIMITATION_ARTICLES
)
from core.court_fee_calculator import (
    calculate_civil_fee, calculate_appeal_fee, calculate_ia_fee,
    calculate_family_fee, calculate_consumer_fee, calculate_drt_fee
)
from core.jurisdiction_validator import validate_jurisdiction
from core.statute_provisions import (
    STATUTES, get_statute, search_provisions, IPC_TO_BNS, CRPC_TO_BNSS
)
from core.prompt_engine import (
    PROMPTS, PROMPT_CATEGORIES, list_prompts, get_prompt, fill_prompt, FIRM_HEADER
)
from core.researcher import search_indian_kanoon, format_research_results


# ─── Page Config ───
st.set_page_config(
    page_title="Drafter & Researcher — D&D Law Associates",
    page_icon="balance_scale",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #555;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    .status-expired { color: #e74c3c; font-weight: 700; }
    .status-critical { color: #e74c3c; font-weight: 700; }
    .status-urgent { color: #e67e22; font-weight: 700; }
    .status-approaching { color: #f39c12; font-weight: 600; }
    .status-within { color: #27ae60; font-weight: 600; }
    .prompt-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        background: #fafafa;
    }
    .prompt-title {
        font-weight: 600;
        font-size: 1.05rem;
        color: #1a1a2e;
    }
    .prompt-desc {
        font-size: 0.9rem;
        color: #666;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    div[data-testid="stSidebar"] .stMarkdown { color: #e0e0e0; }
    div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] h2,
    div[data-testid="stSidebar"] h3 { color: #ffffff; }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar ───
with st.sidebar:
    st.markdown("# D&D Law Associates")
    st.markdown("**Advocates:** DEEPAK ARAVIND.K | DEEPTHI.G")
    st.markdown("Visakhapatnam, AP")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Home",
            "Legal Drafter",
            "Legal Researcher",
            "Limitation Calculator",
            "Court Fee Calculator",
            "Jurisdiction Check",
            "Amount Converter",
            "Statute Reference",
            "IPC to BNS Mapping",
            "Prompt Library",
        ],
        index=0
    )
    st.markdown("---")
    st.markdown("**Quick Tools**")
    st.markdown("Mobile: 7382398999")
    st.markdown("Email: dndlawassociates@gmail.com")


# ═══════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════
if page == "Home":
    st.markdown('<div class="main-header">Drafter & Researcher</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">D&D Law Associates — AI-Powered Legal Drafting & Research Platform</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">30+</div><div class="metric-label">Draft Templates</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">31</div><div class="metric-label">Statutes Embedded</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">40+</div><div class="metric-label">Limitation Articles</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-value">340+</div><div class="metric-label">Key Provisions</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### What This Tool Does")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Legal Drafter**
        - Generate court-ready legal documents
        - 30+ document templates (Plaints, WS, Bail, Notices, Consumer, Family, Appeals, Writs...)
        - D&D Law Associates letterhead on notices
        - Chamber-grade formatting and style

        **Legal Researcher**
        - Search Indian Kanoon for case law
        - 31 statutes with 340+ provisions at your fingertips
        - IPC to BNS / CrPC to BNSS conversion
        - Statute analysis and interpretation
        """)
    with col2:
        st.markdown("""
        **Legal Calculators**
        - Limitation period calculator (40+ articles)
        - AP Court fee calculator (civil, consumer, DRT, family, appeals, IAs)
        - Jurisdiction validator (correct court for Visakhapatnam)
        - Amount converter (Indian legal format — Lakhs/Crores)

        **Prompt Library**
        - 30+ expert prompts for every legal task
        - Fill-in-the-blank prompt generation
        - Copy-paste ready for AI assistants
        - Covers drafting, research, analysis, review
        """)

    st.markdown("---")
    st.info(f"Today: {datetime.now().strftime('%d %B %Y, %A')} | Designed for D&D Law Associates, Visakhapatnam")


# ═══════════════════════════════════════════════
# LEGAL DRAFTER
# ═══════════════════════════════════════════════
elif page == "Legal Drafter":
    st.markdown("## Legal Drafter")
    st.markdown("Generate court-ready legal documents using expert prompts.")

    # Category filter
    categories = {
        "All": None,
        "Drafting": "drafting",
        "Notices": "notices",
        "Criminal": "criminal",
        "Family": "family",
        "Consumer": "consumer",
        "Property": "property",
        "Banking & DRT": "banking",
        "Review": "review",
    }

    selected_cat = st.selectbox("Filter by Category", list(categories.keys()))
    cat_filter = categories[selected_cat]

    # List available prompts
    prompts = list_prompts(category=cat_filter)

    if not prompts:
        st.warning("No prompts found for this category.")
    else:
        # Select prompt
        prompt_options = {p["title"]: p["key"] for p in prompts}
        selected_title = st.selectbox("Select Document Type", list(prompt_options.keys()))
        selected_key = prompt_options[selected_title]
        prompt_data = get_prompt(selected_key)

        st.markdown(f"**Description:** {prompt_data['description']}")
        st.markdown("---")

        # Variable inputs
        st.markdown("### Fill in the Details")
        variables = prompt_data.get("variables", [])
        values = {}

        for var in variables:
            label = var.replace("_", " ").title()
            if var in ("case_facts", "defence_facts", "grounds", "key_terms", "concerns",
                       "draft_text", "document_text", "notice_claims", "client_version",
                       "key_points", "case_details", "debt_details", "grievance",
                       "plaintiff_claims", "our_position", "opposing_stance",
                       "judgment_text_or_citation", "opposing_facts", "arb_clause",
                       "our_case", "context", "relief", "defect_deficiency",
                       "cheque_details", "injury_details", "accident_details",
                       "family_tree", "properties", "security_details",
                       "project_details", "marriage_details", "children_details"):
                values[var] = st.text_area(label, height=150, key=f"var_{var}")
            else:
                values[var] = st.text_input(label, key=f"var_{var}")

        if st.button("Generate Prompt", type="primary", use_container_width=True):
            filled = fill_prompt(selected_key, **values)
            st.markdown("### Generated Prompt")
            st.markdown("*Copy this prompt and paste it into Claude or any AI assistant:*")
            st.code(filled, language="text")
            st.success("Prompt generated! Copy and paste into Claude for a chamber-grade draft.")


# ═══════════════════════════════════════════════
# LEGAL RESEARCHER
# ═══════════════════════════════════════════════
elif page == "Legal Researcher":
    st.markdown("## Legal Researcher")

    tab1, tab2, tab3 = st.tabs(["Case Law Search", "Statute Provisions", "Section Finder"])

    with tab1:
        st.markdown("### Search Indian Kanoon")
        query = st.text_input("Search query (case law, sections, legal issues)", placeholder="e.g., Section 138 NI Act cheque bounce")
        max_results = st.slider("Max results", 5, 20, 10)

        if st.button("Search", key="search_ik"):
            if query:
                with st.spinner("Searching Indian Kanoon..."):
                    results = search_indian_kanoon(query, max_results)
                    if results:
                        for i, r in enumerate(results, 1):
                            if "error" in r:
                                st.error(f"Error: {r['error']}")
                                if "suggestion" in r:
                                    st.info(r["suggestion"])
                            elif "info" in r:
                                st.info(r["info"])
                            else:
                                with st.expander(f"{i}. {r.get('title', 'Untitled')}", expanded=(i <= 3)):
                                    if r.get("court"):
                                        st.markdown(f"**Court:** {r['court']}")
                                    if r.get("url"):
                                        st.markdown(f"**Link:** [{r['url']}]({r['url']})")
                                    if r.get("snippet"):
                                        st.markdown(f"**Summary:** {r['snippet'][:300]}")
            else:
                st.warning("Enter a search query.")

    with tab2:
        st.markdown("### Browse Statute Provisions")
        statute_names = list(STATUTES.keys())
        selected_statute = st.selectbox("Select Statute", statute_names)

        if selected_statute:
            info = STATUTES[selected_statute]
            st.markdown(f"**{info['full_name']}**")
            st.markdown(f"**Module:** {info['module']}")
            st.markdown("---")

            for provision, desc in info["provisions"].items():
                st.markdown(f"**{provision}** — {desc}")

    with tab3:
        st.markdown("### Search Across All Statutes")
        keyword = st.text_input("Search keyword", placeholder="e.g., bail, injunction, maintenance")

        if keyword:
            results = search_provisions(keyword)
            if results:
                st.success(f"Found {len(results)} matching provisions")
                for r in results:
                    st.markdown(f"**{r['statute']}** | {r['provision']} — {r['description']}")
            else:
                st.warning(f"No provisions found matching '{keyword}'")


# ═══════════════════════════════════════════════
# LIMITATION CALCULATOR
# ═══════════════════════════════════════════════
elif page == "Limitation Calculator":
    st.markdown("## Limitation Period Calculator")
    st.markdown("Check if your case is within time — 40+ limitation articles covered.")

    tab1, tab2 = st.tabs(["Calculate", "Browse Articles"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Search for article
            search_key = st.text_input("Search for article type", placeholder="e.g., declaration, cheque, consumer, partition")
            matching = find_articles(search_key) if search_key else list_all_articles()

            article_options = {f"{a['key']} — {a['description'][:60]}": a["key"] for a in matching}
            if article_options:
                selected = st.selectbox("Select Limitation Article", list(article_options.keys()))
                article_key = article_options[selected]
            else:
                st.warning("No matching articles found. Try a different keyword.")
                article_key = None

        with col2:
            coa_date = st.date_input("Date of Cause of Action", value=date.today())

        if article_key and st.button("Calculate Limitation", type="primary", use_container_width=True):
            date_str = coa_date.strftime("%d-%m-%Y")
            result = calculate_limitation(article_key, date_str)

            if "error" in result:
                st.error(result["error"])
            else:
                # Status color
                status = result.get("status", "")
                status_colors = {
                    "EXPIRED": "status-expired",
                    "CRITICAL": "status-critical",
                    "URGENT": "status-urgent",
                    "APPROACHING": "status-approaching",
                    "WITHIN_TIME": "status-within",
                    "NO_LIMITATION": "status-within",
                }
                css_class = status_colors.get(status, "")

                st.markdown("### Result")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Limitation Period", result["limitation_period"])
                with col_b:
                    st.metric("Expiry Date", result["expiry_date"])
                with col_c:
                    days = result["days_remaining"]
                    st.metric("Days Remaining", days if isinstance(days, str) else f"{days} days")

                st.markdown(f'<div class="{css_class}" style="font-size: 1.2rem; padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-top: 1rem;">{status}: {result["urgency"]}</div>', unsafe_allow_html=True)

                with st.expander("Full Details"):
                    for k, v in result.items():
                        st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")

    with tab2:
        st.markdown("### All Limitation Articles")
        articles = list_all_articles()
        for a in articles:
            st.markdown(f"**{a['key']}** — {a['description']} | **Period:** {a['period_text']} | From: {a['from_when']}")


# ═══════════════════════════════════════════════
# COURT FEE CALCULATOR
# ═══════════════════════════════════════════════
elif page == "Court Fee Calculator":
    st.markdown("## AP Court Fee Calculator")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Civil Suit", "Appeal", "IA", "Family", "Consumer/DRT"])

    with tab1:
        st.markdown("### Civil Suit Court Fee")
        suit_type = st.selectbox("Suit Type", ["money", "recovery", "property", "specific_performance", "injunction", "declaration", "partition"])
        suit_value = st.number_input("Suit Value (Rs.)", min_value=0, value=500000, step=10000)

        if st.button("Calculate", key="civil_fee"):
            result = calculate_civil_fee(suit_value, suit_type)
            st.success(f"**Court Fee:** {result['court_fee_formatted']}")
            st.info(f"**Suit Value:** {result['suit_value']}")
            st.markdown(f"*{result['note']}*")
            st.caption(result["disclaimer"])

    with tab2:
        st.markdown("### Appeal Court Fee")
        appeal_type = st.selectbox("Appeal Type", ["first_appeal", "second_appeal", "revision", "criminal_appeal"])
        appeal_value = st.number_input("Suit/Claim Value (Rs.)", min_value=0, value=500000, step=10000, key="appeal_val")

        if st.button("Calculate", key="appeal_fee"):
            result = calculate_appeal_fee(appeal_value, appeal_type)
            st.success(f"**Court Fee:** {result['court_fee_formatted']}")
            st.markdown(f"*{result['note']}*")

    with tab3:
        st.markdown("### Interlocutory Application Fee")
        ia_type = st.selectbox("IA Type", ["general", "injunction", "amendment", "addition_party", "stay", "adjournment", "recall_witness", "appointment_commissioner", "appointment_receiver"])

        if st.button("Calculate", key="ia_fee"):
            result = calculate_ia_fee(ia_type)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"**Court Fee:** {result['court_fee_formatted']}")
                st.markdown(f"*{result['note']}*")

    with tab4:
        st.markdown("### Family Court Fee")
        pet_type = st.selectbox("Petition Type", ["divorce", "mutual_consent_divorce", "rcr", "judicial_separation", "custody", "maintenance", "dv_act"])

        if st.button("Calculate", key="family_fee"):
            result = calculate_family_fee(pet_type)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"**Court Fee:** {result['court_fee_formatted']}")
                st.markdown(f"*{result['note']}*")

    with tab5:
        st.markdown("### Consumer / DRT Fee")
        fee_type = st.radio("Type", ["Consumer", "DRT"])
        claim_value = st.number_input("Claim Value (Rs.)", min_value=0, value=1000000, step=50000, key="cd_val")

        if st.button("Calculate", key="cd_fee"):
            if fee_type == "Consumer":
                result = calculate_consumer_fee(claim_value)
            else:
                result = calculate_drt_fee(claim_value)
            st.success(f"**Court Fee:** {result['court_fee_formatted']}")
            st.markdown(f"*{result['note']}*")


# ═══════════════════════════════════════════════
# JURISDICTION CHECK
# ═══════════════════════════════════════════════
elif page == "Jurisdiction Check":
    st.markdown("## Jurisdiction Validator")
    st.markdown("Find the correct court for your case in Visakhapatnam.")

    col1, col2 = st.columns(2)
    with col1:
        suit_type = st.selectbox("Case Type", ["civil", "criminal", "family", "consumer", "drt", "motor_accident", "rera", "commercial", "cheque_bounce", "ibc"])
    with col2:
        suit_value = st.number_input("Suit/Claim Value (Rs.)", min_value=0, value=500000, step=10000, key="jur_val")

    location = st.text_input("Location", value="Visakhapatnam")

    if st.button("Check Jurisdiction", type="primary", use_container_width=True):
        result = validate_jurisdiction(suit_type, suit_value, location)

        if "error" in result:
            st.error(result["error"])
            if "available_types" in result:
                st.info(f"Available types: {', '.join(result['available_types'])}")
        else:
            st.success(f"**Correct Court:** {result['correct_court']}")
            if "designation" in result:
                st.markdown(f"**Designation:** {result['designation']}")
            if "jurisdiction_type" in result:
                st.markdown(f"**Jurisdiction Type:** {result['jurisdiction_type']}")
            if "pecuniary_limit" in result:
                st.markdown(f"**Pecuniary Limit:** {result['pecuniary_limit']}")
            if "suit_value" in result:
                st.markdown(f"**Suit Value:** {result['suit_value']}")

            if result.get("warnings"):
                st.markdown("### Warnings & Notes")
                for w in result["warnings"]:
                    st.warning(w)


# ═══════════════════════════════════════════════
# AMOUNT CONVERTER
# ═══════════════════════════════════════════════
elif page == "Amount Converter":
    st.markdown("## Indian Legal Amount Converter")
    st.markdown("Convert any amount to Indian legal format (Lakhs/Crores — NOT Millions/Billions).")

    amount = st.number_input("Enter Amount (Rs.)", min_value=0.0, value=500000.0, step=1000.0, format="%.2f")

    if st.button("Convert", type="primary"):
        result = amount_to_legal_format(amount)
        st.markdown(f"### {result}")
        st.code(result, language="text")

    st.markdown("---")
    st.markdown("### Quick Reference")
    examples = [100000, 500000, 1000000, 2500000, 5000000, 10000000, 50000000, 100000000]
    for ex in examples:
        st.markdown(f"**{ex:,}** → {amount_to_legal_format(ex)}")


# ═══════════════════════════════════════════════
# STATUTE REFERENCE
# ═══════════════════════════════════════════════
elif page == "Statute Reference":
    st.markdown("## Statute Quick Reference")
    st.markdown("31 protocol-embedded statutes with 340+ key provisions.")

    # Search across all
    search = st.text_input("Search provisions", placeholder="e.g., bail, injunction, maintenance, cheque")
    if search:
        results = search_provisions(search)
        if results:
            st.success(f"Found {len(results)} provisions matching '{search}'")
            for r in results:
                with st.expander(f"{r['statute']} — {r['provision']}"):
                    st.markdown(r["description"])
        else:
            st.warning(f"No provisions found for '{search}'")
        st.markdown("---")

    # Browse by statute
    for statute_key, statute in STATUTES.items():
        with st.expander(f"{statute_key} — {statute['full_name']} ({statute['module']})"):
            for prov, desc in statute["provisions"].items():
                st.markdown(f"**{prov}:** {desc}")


# ═══════════════════════════════════════════════
# IPC TO BNS MAPPING
# ═══════════════════════════════════════════════
elif page == "IPC to BNS Mapping":
    st.markdown("## IPC to BNS / CrPC to BNSS Mapping")
    st.markdown("Quick conversion from old criminal law sections to new law (2023).")

    tab1, tab2 = st.tabs(["IPC → BNS", "CrPC → BNSS"])

    with tab1:
        st.markdown("### Indian Penal Code → Bharatiya Nyaya Sanhita")
        for ipc, bns in IPC_TO_BNS.items():
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**{ipc}**")
            with col2:
                st.markdown(f"→ **{bns}**")

    with tab2:
        st.markdown("### Code of Criminal Procedure → Bharatiya Nagarik Suraksha Sanhita")
        for crpc, bnss in CRPC_TO_BNSS.items():
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**{crpc}**")
            with col2:
                st.markdown(f"→ **{bnss}**")


# ═══════════════════════════════════════════════
# PROMPT LIBRARY
# ═══════════════════════════════════════════════
elif page == "Prompt Library":
    st.markdown("## Expert Legal Prompt Library")
    st.markdown("30+ ready-to-use prompts for every legal task. Select, fill, copy, paste into Claude.")

    # Category tabs
    all_cats = [("All", None)] + [(v, k) for k, v in PROMPT_CATEGORIES.items()]
    cat_names = [c[0] for c in all_cats]
    selected_tab = st.selectbox("Category", cat_names)
    cat_key = dict(all_cats).get(selected_tab)

    prompts = list_prompts(category=cat_key)

    for p in prompts:
        with st.expander(f"{p['title']} ({p['category'].title()})"):
            st.markdown(f"*{p['description']}*")
            st.markdown(f"**Variables needed:** {', '.join(p['variables']) if p['variables'] else 'None'}")
            prompt_data = get_prompt(p["key"])
            st.code(prompt_data["prompt"][:500] + "..." if len(prompt_data["prompt"]) > 500 else prompt_data["prompt"], language="text")
            if st.button(f"Use this prompt", key=f"use_{p['key']}"):
                st.session_state["selected_prompt"] = p["key"]
                st.info("Go to 'Legal Drafter' page to fill in the details and generate the full prompt.")


# ─── Footer ───
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.85rem;'>"
    "D&D Law Associates | Drafter & Researcher | Built for Advocates DEEPAK ARAVIND.K & DEEPTHI.G"
    "</div>",
    unsafe_allow_html=True
)
