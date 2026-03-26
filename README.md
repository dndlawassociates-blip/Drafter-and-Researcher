# Drafter & Researcher

**D&D Law Associates — AI-Powered Legal Drafting & Research Platform**

A complete legal toolkit for Indian advocates — draft court documents, research case law, calculate limitation periods, court fees, check jurisdiction, and manage your chamber workflow — all from your browser.

## Features

### Legal Drafter
- **25+ Document Templates** — Plaints, Written Statements, Bail Applications, Legal Notices, Consumer Complaints, Family Petitions, Appeals, Execution Petitions, Writ Petitions, and more
- **Smart Preflight Check** — Auto-validates statutes, jurisdiction, limitation before drafting
- **Chamber Style Replication** — Matches your senior advocate's proven drafting patterns from 4,189+ model drafts
- **Indian Legal Format** — Amounts in Lakhs/Crores, proper cause titles, AP court conventions

### Legal Researcher
- **Case Law Search** — Search Indian Kanoon, SCC Online for relevant judgments
- **Statute Lookup** — 31 protocol-embedded statutes with 340+ provisions
- **Bare Act Reference** — Quick access to CPC, BNS, BNSS, BSA, HMA, NI Act, and more
- **Library Search** — Search 4,189+ chamber drafts by keyword

### Legal Calculators
- **Limitation Calculator** — 40+ articles, auto-calculates expiry, flags EXPIRED/CRITICAL/URGENT
- **Court Fee Calculator** — AP courts: civil suits, appeals, IAs, family, consumer, DRT
- **Jurisdiction Validator** — Identifies correct court for Visakhapatnam filings

### Prompt Engine
- **50+ Expert Prompts** — Pre-built prompts for every legal task
- **Case Analysis Prompts** — Strength assessment, risk identification, strategy advice
- **Drafting Prompts** — Chamber-grade document generation
- **Research Prompts** — Targeted legal research queries

## Quick Start

### One-Time Setup
```bash
cd Drafter-and-Researcher
python3.11 -m pip install -r requirements.txt
```

### Run the App
```bash
python3.11 -m streamlit run app.py
```
The app opens in your browser at `http://localhost:8501`

## For D&D Law Associates
- **Advocates:** DEEPAK ARAVIND.K | DEEPTHI.G
- **Office:** Door No. 49-20-5/c, Lalithanagar, Visakhapatnam-16, AP
- **Email:** dndlawassociates@gmail.com | **Mobile:** 7382398999

## Tech Stack
- **Frontend:** Streamlit (Python-based, no JavaScript needed)
- **Backend:** Python 3.11
- **Search:** SQLite FTS5 full-text search
- **AI Integration:** Works with Claude API for AI-powered drafting

## License
Private — D&D Law Associates Internal Tool
