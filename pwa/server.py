"""
D&D Drafter & Researcher — PWA Server
FastAPI backend with all legal tools + Claude AI + Google Drive integration
Run: python3.11 -m uvicorn pwa.server:app --host 0.0.0.0 --port 8000 --reload
"""

import os
import sys
import json
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel

# Add parent to path for core modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.amount_converter import amount_to_legal_format
from core.limitation_calculator import calculate_limitation, find_articles, list_all_articles
from core.court_fee_calculator import (
    calculate_civil_fee, calculate_appeal_fee, calculate_ia_fee,
    calculate_family_fee, calculate_consumer_fee, calculate_drt_fee
)
from core.jurisdiction_validator import validate_jurisdiction
from core.statute_provisions import STATUTES, search_provisions, IPC_TO_BNS, CRPC_TO_BNSS
from core.prompt_engine import PROMPTS, PROMPT_CATEGORIES, list_prompts, fill_prompt
from core.claude_client import draft_document, research_query, analyze_case, review_draft, SYSTEM_PROMPT

app = FastAPI(title="D&D Drafter & Researcher", version="2.0")

# Static files and templates
PWA_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(PWA_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(PWA_DIR, "templates"))


# ─── Pydantic Models ───
class DraftRequest(BaseModel):
    api_key: str
    doc_type: str
    court: str = ""
    parties: str = ""
    facts: str
    relief: str = ""
    additional: str = ""

class ResearchRequest(BaseModel):
    api_key: str
    query: str
    research_type: str = "General Legal Question"

class CaseAnalysisRequest(BaseModel):
    api_key: str
    client_side: str = "Plaintiff"
    case_type: str = "Civil Dispute"
    facts: str
    opponent: str = ""

class ReviewRequest(BaseModel):
    api_key: str
    draft: str
    doc_type: str = "legal document"

class LimitationRequest(BaseModel):
    article_key: str
    coa_date: str

class CourtFeeRequest(BaseModel):
    suit_value: float
    suit_type: str = "money"
    fee_category: str = "civil"

class JurisdictionRequest(BaseModel):
    suit_type: str
    suit_value: float = 0
    location: str = "Visakhapatnam"

class AmountRequest(BaseModel):
    amount: float


# ─── PWA Routes ───
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/manifest.json")
async def manifest():
    return FileResponse(os.path.join(PWA_DIR, "manifest.json"))

@app.get("/sw.js")
async def service_worker():
    return FileResponse(os.path.join(PWA_DIR, "static", "js", "sw.js"), media_type="application/javascript")


# ─── AI API Routes ───
@app.post("/api/draft")
async def api_draft(req: DraftRequest):
    prompt = f"""Draft a {req.doc_type} for filing.

COURT: {req.court or '[To be filled]'}
PARTIES: {req.parties or '[To be filled]'}

FACTS:
{req.facts}

RELIEF SOUGHT:
{req.relief or '[To be specified]'}

ADDITIONAL INSTRUCTIONS:
{req.additional or 'None'}

Generate the COMPLETE document ready for filing — from cause title to signature block.
Include verification clause and supporting affidavit (mandatory for AP courts)."""

    result = draft_document(req.api_key, prompt)
    return {"result": result, "status": "error" if result.startswith("ERROR:") else "ok"}


@app.post("/api/research")
async def api_research(req: ResearchRequest):
    full_query = f"[{req.research_type}]\n\n{req.query}"
    result = research_query(req.api_key, full_query)
    return {"result": result, "status": "error" if result.startswith("ERROR:") else "ok"}


@app.post("/api/analyze")
async def api_analyze(req: CaseAnalysisRequest):
    full_facts = f"""CLIENT POSITION: {req.client_side}
CASE TYPE: {req.case_type}

FACTS:
{req.facts}

OPPOSING POSITION:
{req.opponent or 'Not known yet'}"""
    result = analyze_case(req.api_key, full_facts)
    return {"result": result, "status": "error" if result.startswith("ERROR:") else "ok"}


@app.post("/api/review")
async def api_review(req: ReviewRequest):
    result = review_draft(req.api_key, req.draft, req.doc_type)
    return {"result": result, "status": "error" if result.startswith("ERROR:") else "ok"}


# ─── Calculator API Routes ───
@app.post("/api/limitation")
async def api_limitation(req: LimitationRequest):
    return calculate_limitation(req.article_key, req.coa_date)

@app.get("/api/limitation/articles")
async def api_limitation_articles(keyword: str = ""):
    if keyword:
        return find_articles(keyword)
    return list_all_articles()

@app.post("/api/court-fee")
async def api_court_fee(req: CourtFeeRequest):
    if req.fee_category == "civil":
        return calculate_civil_fee(req.suit_value, req.suit_type)
    elif req.fee_category == "appeal":
        return calculate_appeal_fee(req.suit_value, req.suit_type)
    elif req.fee_category == "ia":
        return calculate_ia_fee(req.suit_type)
    elif req.fee_category == "family":
        return calculate_family_fee(req.suit_type)
    elif req.fee_category == "consumer":
        return calculate_consumer_fee(req.suit_value)
    elif req.fee_category == "drt":
        return calculate_drt_fee(req.suit_value)
    return {"error": "Unknown fee category"}

@app.post("/api/jurisdiction")
async def api_jurisdiction(req: JurisdictionRequest):
    return validate_jurisdiction(req.suit_type, req.suit_value, req.location)

@app.post("/api/amount")
async def api_amount(req: AmountRequest):
    return {"formatted": amount_to_legal_format(req.amount)}


# ─── Reference API Routes ───
@app.get("/api/statutes")
async def api_statutes():
    return {k: {"full_name": v["full_name"], "module": v["module"], "provision_count": len(v["provisions"])} for k, v in STATUTES.items()}

@app.get("/api/statutes/{name}")
async def api_statute_detail(name: str):
    for k, v in STATUTES.items():
        if k.upper() == name.upper():
            return {"statute": k, **v}
    return {"error": f"Statute '{name}' not found"}

@app.get("/api/provisions/search")
async def api_search_provisions(q: str):
    return search_provisions(q)

@app.get("/api/ipc-bns")
async def api_ipc_bns():
    return IPC_TO_BNS

@app.get("/api/crpc-bnss")
async def api_crpc_bnss():
    return CRPC_TO_BNSS

@app.get("/api/prompts")
async def api_prompts(category: str = None):
    return list_prompts(category=category)

@app.get("/api/prompts/{key}")
async def api_prompt_detail(key: str):
    p = PROMPTS.get(key)
    if p:
        return {"key": key, **p}
    return {"error": f"Prompt '{key}' not found"}


# ─── Health ───
@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat(), "version": "2.0",
            "firm": "D&D Law Associates", "statutes": len(STATUTES), "prompts": len(PROMPTS)}
