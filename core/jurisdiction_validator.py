"""AP Jurisdiction Validator — Identifies correct court for filings."""

from .amount_converter import amount_to_legal_format

CIVIL_COURTS = [
    {"name": "Junior Civil Judge Court", "min": 0, "max": 300000, "designation": "Junior Civil Judge"},
    {"name": "Senior Civil Judge Court", "min": 300001, "max": 5000000, "designation": "Senior Civil Judge"},
    {"name": "District Court", "min": 5000001, "max": float("inf"), "designation": "District Judge"},
]

CONSUMER_FORUMS = [
    {"name": "District Consumer Disputes Redressal Forum", "min": 0, "max": 10000000, "designation": "President, DCDRF"},
    {"name": "State Consumer Disputes Redressal Commission", "min": 10000001, "max": 100000000, "designation": "President, SCDRC"},
    {"name": "National Consumer Disputes Redressal Commission", "min": 100000001, "max": float("inf"), "designation": "President, NCDRC"},
]


def validate_jurisdiction(suit_type: str, suit_value: float = 0, location: str = "Visakhapatnam") -> dict:
    warnings = []

    if suit_type == "civil":
        for court in CIVIL_COURTS:
            if court["min"] <= suit_value <= court["max"]:
                return {
                    "correct_court": f"{court['name']}, {location}",
                    "designation": court["designation"],
                    "jurisdiction_type": "Pecuniary + Territorial",
                    "pecuniary_limit": f"Rs.{court['min']:,} to Rs.{court['max']:,}" if court["max"] != float("inf") else f"Above Rs.{court['min']:,}",
                    "suit_value": amount_to_legal_format(suit_value),
                    "warnings": warnings,
                    "location": location
                }

    elif suit_type == "criminal":
        return {
            "correct_court": f"Court of Judicial Magistrate First Class, {location}",
            "designation": "Judicial Magistrate First Class",
            "jurisdiction_type": "Territorial (based on place of offence)",
            "warnings": ["Ensure offence occurred within territorial jurisdiction",
                         "Sessions cases committed by Magistrate to Sessions Court"],
            "location": location
        }

    elif suit_type == "family":
        return {
            "correct_court": f"Family Court, {location}",
            "designation": "Judge, Family Court",
            "jurisdiction_type": "Exclusive — Subject matter",
            "warnings": ["Family Court has EXCLUSIVE jurisdiction — bar on civil court",
                         "No limitation for matrimonial relief (HMA/SMA)",
                         "Territorial: Where parties last resided together OR where wife resides"],
            "location": location
        }

    elif suit_type == "consumer":
        for forum in CONSUMER_FORUMS:
            if forum["min"] <= suit_value <= forum["max"]:
                return {
                    "correct_court": f"{forum['name']}, {location}" if "District" in forum["name"] else forum["name"],
                    "designation": forum["designation"],
                    "jurisdiction_type": "Subject matter + Pecuniary",
                    "pecuniary_limit": f"Up to Rs.{forum['max']:,}" if forum["max"] != float("inf") else f"Above Rs.{forum['min']:,}",
                    "suit_value": amount_to_legal_format(suit_value),
                    "warnings": ["Consumer forum has exclusive jurisdiction — no civil suit for consumer disputes",
                                 "Territorial: Where opposite party resides/works OR where cause of action arose"],
                    "location": location
                }

    elif suit_type == "drt":
        if suit_value >= 1000000:
            return {
                "correct_court": "Debts Recovery Tribunal (DRT)",
                "designation": "Presiding Officer, DRT",
                "jurisdiction_type": "Subject matter + Pecuniary (Rs.10 Lakh+)",
                "suit_value": amount_to_legal_format(suit_value),
                "warnings": ["DRT has EXCLUSIVE jurisdiction for debts Rs.10 Lakh+ — bar on civil court",
                              "SARFAESI challenges also go to DRT",
                              "Appeal lies to DRAT within 30 days"],
                "location": location
            }
        else:
            warnings.append("Debt below Rs.10 Lakh — DRT has NO jurisdiction. File civil suit.")
            return {
                "correct_court": "Civil Court (not DRT — below Rs.10 Lakh threshold)",
                "warnings": warnings
            }

    elif suit_type == "motor_accident":
        return {
            "correct_court": f"Motor Accident Claims Tribunal (MACT), {location}",
            "designation": "Member, MACT",
            "jurisdiction_type": "Exclusive — Subject matter",
            "warnings": ["MACT has EXCLUSIVE jurisdiction — bar on civil court for accident claims",
                         "Limitation: 6 months from accident (liberally condonable)",
                         "Territorial: Where accident occurred"],
            "location": location
        }

    elif suit_type == "rera":
        return {
            "correct_court": "AP-RERA Authority / Adjudicating Officer",
            "designation": "Chairperson, AP-RERA",
            "jurisdiction_type": "Exclusive — Subject matter (real estate)",
            "warnings": ["RERA Authority has exclusive jurisdiction for builder-buyer disputes",
                         "Appeal to RERA Appellate Tribunal within 60 days",
                         "Limitation: 3 years or 1 year from possession (whichever is earlier)"],
            "location": location
        }

    elif suit_type == "commercial":
        if suit_value >= 300000:
            return {
                "correct_court": f"Commercial Court, {location}",
                "designation": "Judge, Commercial Court",
                "jurisdiction_type": "Subject matter + Pecuniary (Rs.3 Lakh+)",
                "suit_value": amount_to_legal_format(suit_value),
                "warnings": ["Commercial Court has jurisdiction for commercial disputes Rs.3 Lakh+",
                              "Mandatory pre-institution mediation for suits (not urgent IAs)"],
                "location": location
            }
        else:
            return {"correct_court": "Civil Court (below Commercial Court threshold)", "warnings": ["Below Rs.3 Lakh — regular civil court"]}

    elif suit_type == "cheque_bounce":
        return {
            "correct_court": f"Court of Judicial Magistrate First Class, {location}",
            "designation": "Judicial Magistrate First Class",
            "jurisdiction_type": "Territorial (where cheque was presented for collection / branch of payee's bank)",
            "warnings": ["Section 138 NI Act — complaint within 30 days of notice period expiry",
                         "Territorial jurisdiction: place where cheque was delivered for collection",
                         "As per Dashrath Rupsingh Rathod — place of branch where cheque presented"],
            "location": location
        }

    elif suit_type == "ibc":
        return {
            "correct_court": "National Company Law Tribunal (NCLT)",
            "designation": "Member, NCLT",
            "jurisdiction_type": "Exclusive — Subject matter (insolvency/bankruptcy)",
            "warnings": ["NCLT has exclusive jurisdiction — moratorium bars all other proceedings",
                         "Section 7 (Financial Creditor) / Section 9 (Operational Creditor) / Section 10 (Corporate Debtor)",
                         "Appeal to NCLAT within 30 days"],
            "location": location
        }

    return {"error": f"Unknown suit type: {suit_type}", "available_types": ["civil", "criminal", "family", "consumer", "drt", "motor_accident", "rera", "commercial", "cheque_bounce", "ibc"]}
