"""Protocol-Embedded Statute Provisions — 31 statutes, 340+ key provisions."""

STATUTES = {
    "CPC": {
        "full_name": "Code of Civil Procedure, 1908",
        "module": "Civil",
        "provisions": {
            "Section 9": "Courts to try all civil suits unless barred",
            "Order 1": "Parties to suits — joinder, misjoinder, non-joinder",
            "Order 6": "Pleadings generally — material facts, not evidence",
            "Order 7": "Plaint — contents, cause of action, jurisdiction, valuation",
            "Order 7 Rule 11": "Rejection of plaint — demurrer, limitation, cause of action",
            "Order 8": "Written Statement — defence, set-off, counter-claim",
            "Order 14": "Settlement of issues — framing of issues from pleadings",
            "Order 18": "Hearing of suit and examination of witnesses",
            "Order 21": "Execution of decrees and orders",
            "Order 22": "Death, marriage and insolvency of parties",
            "Order 26": "Commissions — local investigation, scientific investigation",
            "Order 39": "Temporary injunctions and interlocutory orders",
            "Order 41": "Appeals from original decrees",
            "Order 43": "Appeals from orders",
            "Section 96": "Appeal from original decree",
            "Section 100": "Second appeal on substantial question of law",
            "Section 115": "Revision by High Court",
            "Section 148A": "Caveat — right to be heard before ex-parte order",
            "Section 151": "Inherent powers of the court",
        }
    },
    "BNS": {
        "full_name": "Bharatiya Nyaya Sanhita, 2023 (replaced IPC)",
        "module": "Criminal",
        "provisions": {
            "Chapter II": "General Explanations — definitions, mens rea",
            "Chapter III": "Punishments — fine, imprisonment, community service",
            "Chapter IV": "General Exceptions — mistake of fact, necessity, consent",
            "Chapter V": "Abetment and Criminal Conspiracy",
            "Chapter VI": "Offences against the State",
            "Chapter VII": "Offences against armed forces",
            "Chapter VIII": "Offences against public tranquility",
            "Chapter IX": "Offences by/relating to public servants",
            "Chapter X": "Contempt of lawful authority",
            "Chapter XI": "False evidence and offences against public justice",
            "Chapter XIV": "Offences affecting public health, safety, etc.",
            "Chapter XVII": "Offences against property — theft, extortion, robbery, cheating, mischief",
            "Chapter XVIII": "Offences relating to documents and property marks",
            "Chapter XIX": "Criminal breach of trust and cheating",
            "Section 316-318": "Criminal breach of trust (was IPC 405-409)",
        }
    },
    "BNSS": {
        "full_name": "Bharatiya Nagarik Suraksha Sanhita, 2023 (replaced CrPC)",
        "module": "Criminal",
        "provisions": {
            "Section 144": "Order for maintenance of wives, children and parents (was CrPC 125)",
            "Section 173": "Police report / Chargesheet (was CrPC 173)",
            "Section 193": "Cognizance of offences by Magistrate",
            "Section 223": "Framing of charge",
            "Section 251": "Summary trials",
            "Section 479": "Bail in non-bailable offences",
            "Section 480": "Bail in bailable offences",
            "Section 482": "Anticipatory bail",
            "Section 483": "Bail on default — 60/90 day rule",
            "Section 528": "Quashing of proceedings (was CrPC 482)",
            "Section 530": "Inherent powers of High Court",
            "Section 442": "Appeal against conviction by Magistrate",
            "Section 473": "Transfer of criminal cases",
        }
    },
    "BSA": {
        "full_name": "Bharatiya Sakshya Adhiniyam, 2023 (replaced Evidence Act)",
        "module": "Civil, Criminal, Family",
        "provisions": {
            "Section 2": "Relevant facts — facts in issue and relevant facts",
            "Section 14-19": "Admissions — when binding, proof of",
            "Section 20-26": "Confessions — judicial, extra-judicial, retracted",
            "Section 37-42": "Dying declarations and statements of dead persons",
            "Section 47-53": "Expert opinions — handwriting, science, foreign law",
            "Section 57-63": "Documentary evidence — primary and secondary",
            "Section 61": "Proof of electronic records (was Section 65B)",
            "Section 63": "Special provisions for electronic records — certificate requirement",
            "Section 101": "Burden of proof — who must prove",
            "Section 104": "Burden of proof in civil and criminal cases",
            "Section 118": "Examination-in-chief, cross-examination, re-examination",
            "Section 122-127": "Privileged communications — legal professional, spousal",
        }
    },
    "HMA": {
        "full_name": "Hindu Marriage Act, 1955",
        "module": "Family",
        "provisions": {
            "Section 5": "Conditions for valid Hindu marriage",
            "Section 9": "Restitution of conjugal rights",
            "Section 10": "Judicial separation",
            "Section 11": "Void marriages — bigamy, sapinda, prohibited relationship",
            "Section 12": "Voidable marriages — impotence, fraud, unsoundness",
            "Section 13": "Divorce — cruelty, desertion, conversion, unsound mind, leprosy, VD, renunciation, 7 years unheard of",
            "Section 13-B": "Mutual consent divorce (6-18 month cooling period)",
            "Section 24": "Maintenance pendente lite and litigation expenses",
            "Section 25": "Permanent alimony and maintenance",
            "Section 26": "Custody of children — welfare of minor paramount",
        }
    },
    "NI Act": {
        "full_name": "Negotiable Instruments Act, 1881",
        "module": "Criminal",
        "provisions": {
            "Section 6": "Definition of cheque",
            "Section 138": "Dishonour of cheque — criminal offence (1-2 years imprisonment)",
            "Section 139": "Presumption in favour of holder — legally enforceable debt/liability",
            "Section 140": "Defence that no debt — no defence that discharge was not by cheque drawer",
            "Section 141": "Offences by companies — director/partner liability",
            "Section 142": "Cognizance — complaint within 30 days of cause of action",
            "Section 143": "Power of court to try cases summarily",
            "Section 144": "Mode of service of summons",
            "Section 145": "Evidence on affidavit — examination on commission",
            "Section 147": "Offences compoundable — payee can compound with court permission",
        }
    },
    "DV Act": {
        "full_name": "Protection of Women from Domestic Violence Act, 2005",
        "module": "Family",
        "provisions": {
            "Section 2(a)": "Aggrieved person — wife, live-in partner, mother, sister",
            "Section 3": "Domestic violence — physical, sexual, verbal, emotional, economic abuse",
            "Section 12": "Application to Magistrate — report by Protection Officer",
            "Section 17": "Right to reside in shared household",
            "Section 18": "Protection orders — restraining respondent",
            "Section 19": "Residence orders — shared household, alternative accommodation",
            "Section 20": "Monetary reliefs — compensation, damages, maintenance",
            "Section 21": "Custody orders — temporary custody of children",
            "Section 22": "Compensation orders — mental torture, emotional distress",
            "Section 23": "Ex-parte and interim orders — urgency",
            "Section 29": "Appeal to Court of Session within 30 days",
        }
    },
    "Limitation Act": {
        "full_name": "Limitation Act, 1963",
        "module": "Civil",
        "provisions": {
            "Section 3": "Bar of limitation — court SHALL dismiss if time-barred",
            "Section 5": "Extension of prescribed period — sufficient cause",
            "Section 6-8": "Legal disability — minority, insanity, idiocy",
            "Section 9": "Continuous running of time — once started, no exclusion",
            "Section 12": "Exclusion of time — obtaining copy of decree/order",
            "Section 14": "Exclusion of time of proceeding in wrong court (bona fide)",
            "Section 15": "Exclusion of time of stay/injunction",
            "Section 17": "Effect of fraud or mistake — limitation from discovery",
            "Section 18": "Effect of acknowledgment in writing — fresh start",
            "Section 19": "Effect of payment on limitation for money debts",
            "Section 27": "Extinguishment of right to property — title lost after limitation",
            "Article 58-65": "Specific articles for civil suits",
        }
    },
    "Specific Relief Act": {
        "full_name": "Specific Relief Act, 1963",
        "module": "Civil",
        "provisions": {
            "Section 10": "Specific performance of contract — when granted",
            "Section 12": "Specific performance — parties who may obtain",
            "Section 14": "Contracts not specifically enforceable",
            "Section 16": "Personal bars to relief — readiness and willingness",
            "Section 21": "Power to award compensation in lieu of specific performance",
            "Section 26": "When cancellation may be ordered — voidable contracts",
            "Section 34": "Declaratory decree — declaration of legal character/right",
            "Section 35": "Declaration with consequential relief — plaintiff MUST claim if entitled",
            "Section 36": "Preventive relief — injunctions (temporary and perpetual)",
            "Section 38": "Perpetual injunction — when granted (three-part test)",
            "Section 41": "When injunction refused — acquiescence, delay, conduct",
        }
    },
    "Consumer Protection Act": {
        "full_name": "Consumer Protection Act, 2019",
        "module": "Consumer",
        "provisions": {
            "Section 2(7)": "Consumer — definition (purchases goods/hires services for consideration)",
            "Section 2(11)": "Defect — fault, imperfection, shortcoming in goods",
            "Section 2(12)": "Deficiency — fault, imperfection, inadequacy in service",
            "Section 2(47)": "Unfair trade practice — false representation, misleading advertisement",
            "Section 34": "Jurisdiction of District Forum — territorial + pecuniary",
            "Section 35": "Filing of complaint — manner and form",
            "Section 36": "Admissibility of complaint — limitation 2 years",
            "Section 38": "Procedure on admission of complaint",
            "Section 39": "Findings of forum — reliefs available",
            "Section 40-41": "Appeal to State/National Commission",
            "Section 69": "Product liability — manufacturer, seller, service provider",
        }
    },
    "TPA": {
        "full_name": "Transfer of Property Act, 1882",
        "module": "Civil",
        "provisions": {
            "Section 5": "Transfer of property defined — conveyance, exchange, gift",
            "Section 6": "What may be transferred — spes successionis NOT transferable",
            "Section 17": "Direction regarding accumulation of income void after 18 years",
            "Section 41": "Transfer by ostensible owner — good faith purchaser protection",
            "Section 52": "Doctrine of Lis Pendens — pending suit, no transfer affecting rights",
            "Section 53A": "Part performance — possession + readiness, equity protects",
            "Section 54": "Sale — conveyance of ownership for price",
            "Section 58": "Mortgage — simple, usufructuary, English, equitable, anomalous",
            "Section 105": "Lease of immovable property",
            "Section 106": "Duration and termination of lease — notice requirements",
            "Section 111": "Determination of lease — forfeiture, expiry, notice",
            "Section 114": "Relief against forfeiture — waiver, payment, compliance",
            "Section 122-129": "Gift — transfer without consideration, acceptance, revocation",
        }
    },
    "Contract Act": {
        "full_name": "Indian Contract Act, 1872",
        "module": "Civil",
        "provisions": {
            "Section 2": "Definitions — proposal, promise, agreement, contract",
            "Section 10": "What agreements are contracts — free consent, lawful consideration",
            "Section 14-22": "Free consent — coercion, undue influence, fraud, misrepresentation, mistake",
            "Section 23": "Unlawful consideration and object — void agreements",
            "Section 25": "Agreement without consideration void — exceptions (love, past service, writing)",
            "Section 27": "Agreement in restraint of trade void — exceptions (sale of goodwill)",
            "Section 28": "Agreement in restraint of legal proceedings void",
            "Section 56": "Agreement to do impossible act void — frustration of contract",
            "Section 73": "Compensation for breach — damages",
            "Section 74": "Penalty stipulated — reasonable compensation (Fateh Chand principle)",
            "Section 124-147": "Indemnity and Guarantee — surety, principal debtor, creditor",
            "Section 148-181": "Bailment and Pledge",
            "Section 182-238": "Agency — agent, principal, authority, ratification",
            "Section 2(d)": "Consideration — promise for promise, act for act",
        }
    },
    "Arbitration Act": {
        "full_name": "Arbitration and Conciliation Act, 1996",
        "module": "Civil",
        "provisions": {
            "Section 7": "Arbitration agreement — writing, separate or within contract",
            "Section 8": "Power to refer parties to arbitration — bar on judicial intervention",
            "Section 9": "Interim measures by court — before/during/after arbitration",
            "Section 11": "Appointment of arbitrators — application to court",
            "Section 16": "Competence-competence — tribunal decides its own jurisdiction",
            "Section 17": "Interim measures by arbitral tribunal",
            "Section 21": "Commencement of arbitral proceedings",
            "Section 25": "Default of a party — ex-parte award",
            "Section 29A": "Time limit for arbitral award — 12+6 months",
            "Section 31": "Form and contents of arbitral award",
            "Section 34": "Application for setting aside arbitral award (3 months + 30 days)",
            "Section 36": "Enforcement of arbitral award — execution as decree",
            "Section 37": "Appealable orders — Section 9, 34, 17 orders",
            "Section 45": "Enforcement of foreign awards — New York Convention",
            "Section 87": "Prospective application of 2015/2019 amendments",
            "Section 11(6)": "Appointment of arbitrator by High Court (institutional reference)",
        }
    },
    "Hindu Succession Act": {
        "full_name": "Hindu Succession Act, 1956",
        "module": "Civil, Family",
        "provisions": {
            "Section 4": "Overriding effect — prevails over customs and usage",
            "Section 6": "Devolution of coparcenary property — 2005 Amendment: daughters = sons",
            "Section 8": "General rules of succession — Class I heirs (mother, widow, son, daughter)",
            "Section 9": "Order of succession — Class II heirs when no Class I",
            "Section 10": "Distribution among Class I heirs — per stirpes rule",
            "Section 14": "Property of female Hindu — absolute owner (not limited estate)",
            "Section 15": "General rules of succession for female Hindu intestate",
            "Section 16": "Order of succession of female Hindu",
            "Section 22": "Preferential right to acquire property in certain cases",
            "Section 23": "Right of daughter to reside in dwelling house (repealed 2005)",
            "Section 30": "Power to will — any Hindu may dispose by will or codicil",
        }
    },
    "Motor Vehicles Act": {
        "full_name": "Motor Vehicles Act, 1988",
        "module": "Civil",
        "provisions": {
            "Section 3": "Necessity for driving licence",
            "Section 140": "Liability to pay compensation — no-fault principle",
            "Section 163A": "Special provisions for third party claims — structured formula",
            "Section 166": "Application for compensation — MACT claim",
            "Section 168": "Award by Claims Tribunal",
            "Section 169": "Procedure for hearing — Motor Accident Claims Tribunal",
            "Section 170": "Impleading insurer — mandatory party",
            "Section 173": "Appeal — within 90 days to High Court",
            "Section 147": "Requirements of third party insurance policy",
            "Section 149": "Duty of insurers to satisfy judgments against insured",
            "Sarla Verma": "Multiplier method for future loss (Supreme Court guideline)",
            "Pranay Sethi": "Conventional heads — funeral, loss of estate, consortium",
            "Section 158(6)": "Accident Information Report — Motor Accident Database",
            "Section 164": "Payment of compensation on structured formula basis",
        }
    },
    "RERA Act": {
        "full_name": "Real Estate (Regulation and Development) Act, 2016",
        "module": "Civil, Consumer",
        "provisions": {
            "Section 3": "Registration of real estate project — mandatory",
            "Section 4": "Application for registration — documents + layout plan",
            "Section 11": "Obligations of promoter — timely delivery, defects liability",
            "Section 12": "Obligations of promoter regarding insurance of real estate project",
            "Section 14": "Adherence to sanctioned plans — no modification without consent",
            "Section 18": "Return of amount/interest — delay in possession",
            "Section 19": "Rights of allottee",
            "Section 31": "Complaint to Authority — filing procedure",
            "Section 35": "Powers of Authority",
            "Section 38": "Adjudicating Officers for compensation",
            "Section 43": "Appeal to Appellate Tribunal — within 60 days",
            "Section 44": "Appeal to High Court — within 60 days from Appellate Tribunal",
            "Section 59-72": "Penalties and offences",
            "Section 79": "Bar on civil court — RERA exclusive",
            "Section 81": "Act to have overriding effect",
        }
    },
    "RDDBFI Act": {
        "full_name": "Recovery of Debts and Bankruptcy Act, 1993 (DRT Act)",
        "module": "Civil",
        "provisions": {
            "Section 3": "Establishment of Debt Recovery Tribunals",
            "Section 17": "Jurisdiction — debts Rs.10 Lakh and above",
            "Section 18": "Bar on civil court — DRT exclusive for covered debts",
            "Section 19": "Application to DRT — form, fee, limitation",
            "Section 20": "Power of Tribunal — civil court powers",
            "Section 22": "Limitation for applications — Limitation Act applies",
            "Section 25": "Recovery Officers — execution of recovery certificate",
            "Section 27": "Appeal to DRAT within 30 days",
            "Section 28": "Procedure of DRAT",
            "Section 30": "Transfer of pending cases from civil courts",
            "Section 31": "Power of Chairman to transfer cases between DRTs",
            "Section 34": "Act to have overriding effect (Mardia Chemicals — partly)",
            "Section 36": "Application of CPC — procedure before Tribunal",
        }
    },
    "SARFAESI Act": {
        "full_name": "Securitisation and Reconstruction of Financial Assets Act, 2002",
        "module": "Civil",
        "provisions": {
            "Section 13": "Enforcement of security interest — notice to borrower",
            "Section 13(2)": "60-day notice — demanding payment of secured debt",
            "Section 13(3A)": "Notice to guarantor — simultaneous notice",
            "Section 13(4)": "Measures after 60-day notice — possession, sale, management",
            "Section 14": "Chief Metropolitan Magistrate — assistance in taking possession",
            "Section 17": "Application to DRT — appeal against secured creditor's action (45 days)",
            "Section 17(1)": "Any person aggrieved — borrower, guarantor, third party",
            "Section 18": "Appeal to DRAT within 30 days — deposit of 50% or tribunal may reduce",
            "Section 26E": "Priority of secured creditors over government dues",
            "Section 29": "Offences — contravention of provisions",
            "Section 31B": "Application of other laws not barred",
            "Section 34": "Bar on civil court jurisdiction for SARFAESI matters",
            "Section 37": "SARFAESI applies to NPA classification by RBI guidelines",
        }
    },
    "Indian Succession Act": {
        "full_name": "Indian Succession Act, 1925",
        "module": "Civil",
        "provisions": {
            "Section 57": "Application for probate — executor named in will",
            "Section 59": "Will by any person of sound mind, 18+ years",
            "Section 63": "Execution of unprivileged will — signed, attested by 2+ witnesses",
            "Section 213": "Right as executor/legatee — probate or letters of administration",
            "Section 218": "Grant of probate — court satisfied of genuineness",
            "Section 222": "Caveat against grant — objection to probate",
            "Section 263-267": "Letters of administration — when no will/executor",
            "Section 270": "Bond required for administration",
            "Section 282-290": "Succession certificate — debts and securities",
            "Section 370-390": "Administration of assets — payment of debts, distribution",
            "Section 57-63": "Wills — capacity, revocation, construction",
            "Section 74": "Privileged wills — soldiers and mariners",
            "Section 276": "General power of administrator — same as executor",
        }
    },
    "Registration Act": {
        "full_name": "Registration Act, 1908",
        "module": "Civil",
        "provisions": {
            "Section 17": "Documents of which registration is compulsory — sale, gift, lease 1yr+, mortgage",
            "Section 18": "Documents of which registration is optional",
            "Section 23": "Time for presenting documents — 4 months from execution",
            "Section 25": "Condonation of delay — up to 4 more months with fine",
            "Section 32": "Persons to present documents — executant or representative",
            "Section 34": "Enquiry before registration — identity of executant",
            "Section 35": "Procedure on admission/denial of execution",
            "Section 47": "Time from which registered document operates",
            "Section 49": "Effect of non-registration — not admissible as evidence of transaction",
            "Section 77": "Certified copies — evidentiary value, right to inspect",
        }
    },
    "IBC": {
        "full_name": "Insolvency and Bankruptcy Code, 2016",
        "module": "Civil",
        "provisions": {
            "Section 4": "Applicability — minimum default Rs.1 Crore (COVID notification)",
            "Section 5(7)": "Financial creditor — disbursed against time value of money",
            "Section 5(20)": "Operational creditor — goods/services claim",
            "Section 7": "Initiation by financial creditor — NCLT application",
            "Section 9": "Initiation by operational creditor — demand notice + NCLT",
            "Section 10": "Initiation by corporate debtor — voluntary insolvency",
            "Section 14": "Moratorium — bar on all proceedings during CIRP",
            "Section 16": "Appointment of Interim Resolution Professional (IRP)",
            "Section 21": "Committee of Creditors (CoC) — 66% majority for resolution plan",
            "Section 29A": "Persons not eligible to submit resolution plan — disqualifications",
            "Section 30": "Submission and approval of resolution plan",
            "Section 31": "Approval of resolution plan by NCLT — binding on all stakeholders",
            "Section 33": "Liquidation order — when no resolution plan approved",
            "Section 61": "Appeals to NCLAT — within 30 days",
            "Section 238": "Overriding effect — IBC prevails over other laws",
        }
    },
    "NDPS Act": {
        "full_name": "Narcotic Drugs and Psychotropic Substances Act, 1985",
        "module": "Criminal",
        "provisions": {
            "Section 8": "Prohibition of certain operations — production, manufacture, sale",
            "Section 15": "Punishment for contravention re: poppy straw",
            "Section 20": "Punishment for cannabis — small/commercial quantity distinction",
            "Section 21": "Punishment for manufactured drugs",
            "Section 22": "Punishment for psychotropic substances",
            "Section 27": "Punishment for consumption — 1 year or fine or both",
            "Section 31A": "Death penalty for repeat offenders of certain quantities",
            "Section 35": "Presumption of culpable mental state",
            "Section 36A": "Offences triable by Special Courts exclusively",
            "Section 37": "Bail restrictions — twin conditions (reasonable grounds + no re-offend)",
            "Section 42": "Power of entry, search, seizure and arrest (empowerment certificate)",
            "Section 43": "Power of seizure in public places",
            "Section 50": "Conditions for search of persons — right to be searched before Magistrate/gazetted officer",
            "Section 52A": "Disposal of seized drugs — sampling + destruction",
            "Section 54": "Presumption from possession — burden on accused",
            "Section 64A": "Immunity to addict volunteering for treatment",
            "Section 67": "Power to call for information — not admissible as confession (Tofan Singh)",
        }
    },
    "Guardians & Wards Act": {
        "full_name": "Guardians and Wards Act, 1890",
        "module": "Family",
        "provisions": {
            "Section 7": "Power of the court to make order as to guardianship",
            "Section 9": "Court having jurisdiction to appoint guardian — District Court",
            "Section 17": "Matters to be considered by court — welfare of minor paramount",
            "Section 19": "Guardian not to be appointed by court in certain cases",
            "Section 25": "Title of guardian to custody of ward",
            "Section 39-41": "Removal and discharge of guardians",
        }
    },
    "SMA": {
        "full_name": "Special Marriage Act, 1954",
        "module": "Family",
        "provisions": {
            "Section 4": "Conditions for special marriage — age, consent, prohibited degrees",
            "Section 5-8": "Notice and objection procedure",
            "Section 15": "Registration of foreign marriages",
            "Section 27": "Divorce on specific grounds (similar to HMA Section 13)",
            "Section 28": "Mutual consent divorce (6 months cooling period)",
            "Section 36-38": "Alimony and maintenance, custody, appeals",
        }
    },
    "AP Tenancy Act": {
        "full_name": "AP Buildings (Lease, Rent and Eviction Control) Act, 1960",
        "module": "Civil",
        "provisions": {
            "Section 3": "Fixation of fair rent",
            "Section 4": "Information to be given about vacancy",
            "Section 5": "Allotment of buildings in possession of landlord",
            "Section 10": "Eviction of tenants — grounds",
            "Section 10(2)(i)": "Default in payment of rent",
            "Section 10(2)(ii)": "Subletting without consent",
            "Section 10(2)(iii)": "Nuisance/using premises for immoral purposes",
            "Section 10(3)(a)": "Bona fide personal requirement",
            "Section 10(3)(c)": "Demolition and reconstruction",
            "Section 13": "Deposit of rent in court (when landlord refuses)",
            "Section 19": "Bar on civil court — Rent Controller exclusive",
        }
    },
}

# Legacy mappings
IPC_TO_BNS = {
    "IPC 302 (Murder)": "BNS Section 103",
    "IPC 304 (Culpable homicide)": "BNS Section 105",
    "IPC 304A (Death by negligence)": "BNS Section 106",
    "IPC 306 (Abetment of suicide)": "BNS Section 108",
    "IPC 307 (Attempt to murder)": "BNS Section 109",
    "IPC 323 (Hurt)": "BNS Section 115",
    "IPC 354 (Assault on woman)": "BNS Section 74",
    "IPC 376 (Rape)": "BNS Section 64",
    "IPC 406 (Criminal breach of trust)": "BNS Section 316",
    "IPC 420 (Cheating)": "BNS Section 318",
    "IPC 498A (Cruelty by husband)": "BNS Section 85",
    "IPC 499/500 (Defamation)": "BNS Section 356",
    "IPC 504 (Intentional insult)": "BNS Section 352",
    "IPC 506 (Criminal intimidation)": "BNS Section 351",
    "IPC 509 (Outraging modesty)": "BNS Section 79",
}

CRPC_TO_BNSS = {
    "CrPC 125 (Maintenance)": "BNSS Section 144",
    "CrPC 154 (FIR)": "BNSS Section 173",
    "CrPC 161 (Police statement)": "BNSS Section 180",
    "CrPC 164 (Confession before Magistrate)": "BNSS Section 183",
    "CrPC 190 (Cognizance)": "BNSS Section 210",
    "CrPC 200 (Complaint)": "BNSS Section 223",
    "CrPC 227/228 (Discharge/Charge)": "BNSS Section 250/251",
    "CrPC 313 (Examination of accused)": "BNSS Section 346",
    "CrPC 354 (Sentence)": "BNSS Section 392",
    "CrPC 374 (Appeal)": "BNSS Section 411",
    "CrPC 397 (Revision)": "BNSS Section 442",
    "CrPC 437 (Bail non-bailable)": "BNSS Section 479",
    "CrPC 438 (Anticipatory bail)": "BNSS Section 482",
    "CrPC 439 (Special bail powers)": "BNSS Section 483",
    "CrPC 482 (Inherent powers)": "BNSS Section 528",
    "CrPC 167 (Remand/default bail)": "BNSS Section 187",
}


def get_statute(name: str) -> dict:
    key = name.upper().strip()
    for k, v in STATUTES.items():
        if k.upper() == key or key in v["full_name"].upper():
            return {"statute": k, **v}
    return {"error": f"Statute '{name}' not found. Available: {', '.join(STATUTES.keys())}"}


def search_provisions(keyword: str) -> list:
    keyword_lower = keyword.lower()
    results = []
    for statute_key, statute in STATUTES.items():
        for provision, desc in statute["provisions"].items():
            if keyword_lower in provision.lower() or keyword_lower in desc.lower():
                results.append({
                    "statute": statute_key,
                    "provision": provision,
                    "description": desc
                })
    return results


def get_ipc_to_bns(ipc_section: str = None) -> dict:
    if ipc_section:
        for k, v in IPC_TO_BNS.items():
            if ipc_section.lower() in k.lower():
                return {"ipc": k, "bns": v}
        return {"error": f"IPC section '{ipc_section}' not found in mapping"}
    return IPC_TO_BNS


def get_crpc_to_bnss(crpc_section: str = None) -> dict:
    if crpc_section:
        for k, v in CRPC_TO_BNSS.items():
            if crpc_section.lower() in k.lower():
                return {"crpc": k, "bnss": v}
        return {"error": f"CrPC section '{crpc_section}' not found in mapping"}
    return CRPC_TO_BNSS
