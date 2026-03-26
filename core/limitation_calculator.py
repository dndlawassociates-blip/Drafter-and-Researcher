"""Limitation Period Calculator — 40+ articles for Indian courts."""

from datetime import datetime, timedelta
from typing import Optional

LIMITATION_ARTICLES = {
    # Civil Suits
    "58": {"description": "Suit for declaration (Section 34 SRA)", "period_days": 1095, "period_text": "3 years", "from_when": "When right to sue first accrues"},
    "54": {"description": "Suit for specific performance", "period_days": 1095, "period_text": "3 years", "from_when": "Date fixed for performance / when plaintiff has notice of refusal"},
    "55": {"description": "Suit for compensation for breach of contract", "period_days": 1095, "period_text": "3 years", "from_when": "When contract is broken"},
    "56": {"description": "Suit on account stated", "period_days": 1095, "period_text": "3 years", "from_when": "When the account is stated in writing signed by defendant"},
    "62": {"description": "Suit for money payable for money lent", "period_days": 1095, "period_text": "3 years", "from_when": "When the loan is made"},
    "65": {"description": "Suit for compensation for tort/wrong", "period_days": 1095, "period_text": "3 years", "from_when": "When the wrong is committed"},
    "113": {"description": "Any suit for which no limitation is provided (residuary)", "period_days": 1095, "period_text": "3 years", "from_when": "When right to sue accrues"},
    "59": {"description": "Suit for possession of immovable property (title)", "period_days": 4380, "period_text": "12 years", "from_when": "When possession becomes adverse"},
    "64": {"description": "Suit for price of goods sold and delivered", "period_days": 1095, "period_text": "3 years", "from_when": "When goods are delivered"},
    "1": {"description": "Suit relating to accounts — for balance due on mutual, open and current account", "period_days": 1095, "period_text": "3 years", "from_when": "Close of year in which last item admitted/proved is entered"},

    # Injunction
    "injunction_permanent": {"description": "Suit for permanent injunction", "period_days": 1095, "period_text": "3 years", "from_when": "When right to sue first accrues (continuing wrong — fresh cause each day)"},

    # Partition
    "partition": {"description": "Suit for partition", "period_days": 4380, "period_text": "12 years (no limitation for coparcener)", "from_when": "When exclusion from joint property occurs"},

    # Recovery of Money
    "recovery_money": {"description": "Suit for recovery of money due under contract", "period_days": 1095, "period_text": "3 years", "from_when": "When money becomes due"},

    # Appeals
    "115": {"description": "Appeal from decree of any court (first appeal)", "period_days": 90, "period_text": "90 days", "from_when": "Date of decree"},
    "116": {"description": "Appeal to High Court (second appeal)", "period_days": 90, "period_text": "90 days", "from_when": "Date of decree appealed from"},
    "117": {"description": "Appeal from order (appealable orders)", "period_days": 30, "period_text": "30 days", "from_when": "Date of order"},

    # Applications
    "137": {"description": "Any other application (residuary)", "period_days": 1095, "period_text": "3 years", "from_when": "When right to apply accrues"},
    "execution": {"description": "Application for execution of decree", "period_days": 4380, "period_text": "12 years", "from_when": "Date of decree or last order on execution"},

    # Criminal
    "131": {"description": "Criminal revision to High Court", "period_days": 90, "period_text": "90 days", "from_when": "Date of order sought to be revised"},
    "132": {"description": "Criminal appeal to Sessions/High Court", "period_days": 30, "period_text": "30 days", "from_when": "Date of sentence or order"},

    # NI Act
    "ni_138_complaint": {"description": "Complaint under Section 138 NI Act (cheque bounce)", "period_days": 30, "period_text": "30 days (after 15-day notice period)", "from_when": "Expiry of 15 days from receipt of legal notice by drawer"},
    "ni_138_notice": {"description": "Legal notice under Section 138 NI Act", "period_days": 30, "period_text": "30 days", "from_when": "Date of receiving 'return memo' from bank"},

    # Consumer
    "consumer_complaint": {"description": "Consumer complaint under CPA 2019", "period_days": 730, "period_text": "2 years", "from_when": "Date of cause of action (defect/deficiency)"},
    "consumer_appeal": {"description": "Appeal from Consumer Forum order", "period_days": 30, "period_text": "30 days", "from_when": "Date of order appealed against"},

    # DRT/Banking
    "drt_oa": {"description": "DRT Original Application (recovery of debt)", "period_days": 1095, "period_text": "3 years", "from_when": "Date when debt becomes due / NPA date"},
    "sarfaesi_challenge": {"description": "Challenge to SARFAESI action under Section 17", "period_days": 45, "period_text": "45 days", "from_when": "Date of action taken by secured creditor"},

    # Motor Accident
    "mact_166": {"description": "MACT claim (Motor Accident Compensation)", "period_days": 180, "period_text": "6 months (liberally condonable)", "from_when": "Date of accident"},

    # Family
    "divorce": {"description": "Divorce petition (HMA/SMA)", "period_days": 0, "period_text": "No limitation (but grounds must subsist)", "from_when": "N/A — No limitation for matrimonial relief"},
    "maintenance_125": {"description": "Maintenance under Section 144 BNSS", "period_days": 0, "period_text": "No limitation", "from_when": "N/A"},
    "dv_act": {"description": "Application under DV Act 2005", "period_days": 0, "period_text": "No limitation (continuing wrong)", "from_when": "N/A — domestic violence is a continuing wrong"},
    "custody": {"description": "Custody petition under GW Act / HMA", "period_days": 0, "period_text": "No limitation", "from_when": "N/A"},

    # RERA
    "rera_complaint": {"description": "RERA complaint under Section 31", "period_days": 1095, "period_text": "3 years (or 1 year from possession — earlier)", "from_when": "Date of cause of action"},

    # IBC
    "ibc_application": {"description": "IBC application (Section 7/9/10)", "period_days": 1095, "period_text": "3 years (from default/NPA date)", "from_when": "Date of default as per Part III Schedule"},

    # Arbitration
    "arb_34": {"description": "Challenge to arbitral award (Section 34)", "period_days": 90, "period_text": "3 months (+ 30 days condonable)", "from_when": "Date of receipt of arbitral award"},
    "arb_9": {"description": "Interim relief application (Section 9)", "period_days": 0, "period_text": "No limitation (before/during/after arbitration)", "from_when": "N/A"},

    # Writ Petition
    "writ_petition": {"description": "Writ Petition (Article 226/32)", "period_days": 0, "period_text": "No limitation (but laches/delay can be fatal)", "from_when": "Should be filed without unreasonable delay"},
}


def calculate_limitation(article_key: str, cause_of_action_date: str) -> dict:
    article = LIMITATION_ARTICLES.get(article_key)
    if not article:
        return {"error": f"Article '{article_key}' not found. Use find_articles() to search."}

    try:
        coa_date = datetime.strptime(cause_of_action_date, "%d-%m-%Y")
    except ValueError:
        return {"error": "Date must be in DD-MM-YYYY format"}

    result = {
        "article": article_key,
        "description": article["description"],
        "limitation_period": article["period_text"],
        "from_when": article["from_when"],
        "cause_of_action_date": coa_date.strftime("%d-%m-%Y"),
    }

    if article["period_days"] == 0:
        result["expiry_date"] = "NO LIMITATION"
        result["days_remaining"] = "N/A"
        result["status"] = "NO_LIMITATION"
        result["urgency"] = "No time bar — but avoid unreasonable delay"
        return result

    expiry = coa_date + timedelta(days=article["period_days"])
    today = datetime.now()
    remaining = (expiry - today).days

    result["expiry_date"] = expiry.strftime("%d-%m-%Y")
    result["days_remaining"] = remaining

    if remaining < 0:
        result["status"] = "EXPIRED"
        result["urgency"] = f"EXPIRED {abs(remaining)} days ago! Seek condonation of delay if available."
    elif remaining <= 7:
        result["status"] = "CRITICAL"
        result["urgency"] = f"CRITICAL — Only {remaining} days left! File IMMEDIATELY."
    elif remaining <= 30:
        result["status"] = "URGENT"
        result["urgency"] = f"URGENT — {remaining} days remaining. Prepare and file without delay."
    elif remaining <= 90:
        result["status"] = "APPROACHING"
        result["urgency"] = f"Approaching — {remaining} days remaining. Begin preparation."
    else:
        result["status"] = "WITHIN_TIME"
        result["urgency"] = f"Within time — {remaining} days remaining."

    return result


def find_articles(keyword: str) -> list:
    keyword_lower = keyword.lower()
    results = []
    for key, article in LIMITATION_ARTICLES.items():
        if keyword_lower in article["description"].lower() or keyword_lower in key.lower():
            results.append({"key": key, **article})
    return results


def list_all_articles() -> list:
    return [{"key": k, **v} for k, v in LIMITATION_ARTICLES.items()]
