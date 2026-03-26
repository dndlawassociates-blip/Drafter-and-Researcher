"""AP Court Fee Calculator — Civil suits, appeals, IAs, family, consumer, DRT."""

from .amount_converter import amount_to_legal_format


def calculate_civil_fee(suit_value: float, suit_type: str = "money") -> dict:
    """Calculate court fee for civil suits in AP courts."""
    fee = 0.0
    note = ""

    if suit_type in ("money", "recovery", "property", "specific_performance"):
        # Ad valorem — AP Court Fee Act schedule
        remaining = suit_value
        if remaining > 0:
            slab = min(remaining, 100000)
            fee += slab * 0.075  # 7.5% up to 1 Lakh
            remaining -= slab
        if remaining > 0:
            slab = min(remaining, 400000)
            fee += slab * 0.05  # 5% from 1L to 5L
            remaining -= slab
        if remaining > 0:
            slab = min(remaining, 500000)
            fee += slab * 0.04  # 4% from 5L to 10L
            remaining -= slab
        if remaining > 0:
            slab = min(remaining, 1500000)
            fee += slab * 0.03  # 3% from 10L to 25L
            remaining -= slab
        if remaining > 0:
            fee += remaining * 0.02  # 2% above 25L
        note = "Ad valorem court fee under AP Court Fees Act"

    elif suit_type == "injunction":
        fee = 500
        note = "Fixed court fee for permanent injunction suit"

    elif suit_type == "declaration":
        if suit_value > 0:
            fee = calculate_civil_fee(suit_value, "money")["court_fee"]
            note = "Declaration with consequential relief — ad valorem on suit value"
        else:
            fee = 500
            note = "Declaration without consequential relief — fixed fee"

    elif suit_type == "partition":
        # Ad valorem on plaintiff's share value
        fee = calculate_civil_fee(suit_value, "money")["court_fee"]
        note = "Court fee on plaintiff's share value (ad valorem)"

    else:
        fee = calculate_civil_fee(suit_value, "money")["court_fee"]
        note = f"Default ad valorem calculation for '{suit_type}'"

    fee = max(fee, 100)  # Minimum court fee

    return {
        "suit_type": suit_type,
        "suit_value": amount_to_legal_format(suit_value),
        "court_fee": round(fee),
        "court_fee_formatted": amount_to_legal_format(round(fee)),
        "note": note,
        "disclaimer": "Verify exact fee with court office — rates may vary by notification"
    }


def calculate_appeal_fee(suit_value: float, appeal_type: str = "first_appeal") -> dict:
    if appeal_type == "first_appeal":
        base = calculate_civil_fee(suit_value, "money")
        return {**base, "note": "First appeal — same court fee as original suit", "appeal_type": appeal_type}
    elif appeal_type == "second_appeal":
        base = calculate_civil_fee(suit_value, "money")
        base["court_fee"] = round(base["court_fee"] * 0.5)
        base["court_fee_formatted"] = amount_to_legal_format(base["court_fee"])
        base["note"] = "Second appeal — 50% of original court fee"
        base["appeal_type"] = appeal_type
        return base
    elif appeal_type == "revision":
        return {"court_fee": 500, "court_fee_formatted": amount_to_legal_format(500), "note": "Revision petition — fixed fee Rs.500", "appeal_type": appeal_type}
    elif appeal_type == "criminal_appeal":
        return {"court_fee": 50, "court_fee_formatted": amount_to_legal_format(50), "note": "Criminal appeal — fixed fee Rs.50", "appeal_type": appeal_type}
    return {"error": f"Unknown appeal type: {appeal_type}"}


def calculate_ia_fee(ia_type: str = "general") -> dict:
    fees = {
        "general": (100, "General IA — Rs.100"),
        "injunction": (200, "Interim Injunction (Order 39) — Rs.200"),
        "amendment": (100, "Amendment of plaint/WS — Rs.100"),
        "addition_party": (100, "Addition/deletion of party — Rs.100"),
        "stay": (200, "Stay application — Rs.200"),
        "adjournment": (50, "Adjournment application — Rs.50"),
        "recall_witness": (100, "Recall of witness — Rs.100"),
        "appointment_commissioner": (200, "Appointment of Commissioner — Rs.200"),
        "appointment_receiver": (200, "Appointment of Receiver — Rs.200"),
    }
    if ia_type in fees:
        fee, note = fees[ia_type]
        return {"ia_type": ia_type, "court_fee": fee, "court_fee_formatted": amount_to_legal_format(fee), "note": note}
    return {"error": f"Unknown IA type: {ia_type}. Options: {', '.join(fees.keys())}"}


def calculate_family_fee(petition_type: str) -> dict:
    fees = {
        "divorce": (500, "Divorce petition — Rs.500"),
        "mutual_consent_divorce": (500, "Mutual consent divorce — Rs.500"),
        "rcr": (500, "Restitution of Conjugal Rights — Rs.500"),
        "judicial_separation": (500, "Judicial Separation — Rs.500"),
        "custody": (500, "Custody petition — Rs.500"),
        "maintenance": (0, "Maintenance petition — Court fee NIL"),
        "dv_act": (0, "DV Act application — Court fee NIL"),
    }
    if petition_type in fees:
        fee, note = fees[petition_type]
        return {"petition_type": petition_type, "court_fee": fee, "court_fee_formatted": amount_to_legal_format(fee) if fee > 0 else "NIL", "note": note}
    return {"error": f"Unknown petition type: {petition_type}. Options: {', '.join(fees.keys())}"}


def calculate_consumer_fee(claim_value: float) -> dict:
    if claim_value <= 500000:
        fee = 0
        note = "Up to Rs.5 Lakh — NIL court fee"
    elif claim_value <= 1000000:
        fee = 2000
        note = "Rs.5L to Rs.10L — Rs.2,000"
    elif claim_value <= 2000000:
        fee = 3000
        note = "Rs.10L to Rs.20L — Rs.3,000"
    elif claim_value <= 5000000:
        fee = 5000
        note = "Rs.20L to Rs.50L — Rs.5,000"
    elif claim_value <= 10000000:
        fee = 10000
        note = "Rs.50L to Rs.1 Cr — Rs.10,000"
    elif claim_value <= 100000000:
        fee = 25000
        note = "Rs.1 Cr to Rs.10 Cr — Rs.25,000"
    else:
        fee = 50000
        note = "Above Rs.10 Cr — Rs.50,000"

    return {
        "claim_value": amount_to_legal_format(claim_value),
        "court_fee": fee,
        "court_fee_formatted": amount_to_legal_format(fee) if fee > 0 else "NIL",
        "note": note
    }


def calculate_drt_fee(claim_value: float) -> dict:
    """DRT OA filing fee calculation."""
    if claim_value <= 1000000:
        fee = 12000
    elif claim_value <= 5000000:
        fee = 12000 + (claim_value - 1000000) * 0.01
    elif claim_value <= 10000000:
        fee = 52000 + (claim_value - 5000000) * 0.005
    elif claim_value <= 50000000:
        fee = 77000 + (claim_value - 10000000) * 0.0025
    else:
        fee = 177000 + (claim_value - 50000000) * 0.001

    fee = min(fee, 500000)  # Cap at Rs.5 Lakh

    return {
        "claim_value": amount_to_legal_format(claim_value),
        "court_fee": round(fee),
        "court_fee_formatted": amount_to_legal_format(round(fee)),
        "note": "DRT OA fee (RDDBFI Act) — capped at Rs.5,00,000/-"
    }
