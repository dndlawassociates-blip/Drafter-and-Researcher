"""Indian Legal Amount Converter — Lakhs/Crores format only."""


ONES = [
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen"
]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]


def _two_digits(n: int) -> str:
    if n < 20:
        return ONES[n]
    t, o = divmod(n, 10)
    return f"{TENS[t]} {ONES[o]}".strip()


def number_to_words_indian(n: int) -> str:
    if n == 0:
        return "Zero"
    if n < 0:
        return "Minus " + number_to_words_indian(-n)

    parts = []
    # Crores
    if n >= 10000000:
        crores = n // 10000000
        parts.append(f"{number_to_words_indian(crores)} Crore")
        n %= 10000000
    # Lakhs
    if n >= 100000:
        lakhs = n // 100000
        parts.append(f"{_two_digits(lakhs)} Lakh")
        n %= 100000
    # Thousands
    if n >= 1000:
        thousands = n // 1000
        parts.append(f"{_two_digits(thousands)} Thousand")
        n %= 1000
    # Hundreds
    if n >= 100:
        hundreds = n // 100
        parts.append(f"{ONES[hundreds]} Hundred")
        n %= 100
    # Remaining
    if n > 0:
        parts.append(_two_digits(n))

    return " ".join(parts)


def format_indian_number(n: int) -> str:
    s = str(n)
    if len(s) <= 3:
        return s
    last3 = s[-3:]
    rest = s[:-3]
    groups = []
    while rest:
        groups.append(rest[-2:])
        rest = rest[:-2]
    groups.reverse()
    return ",".join(groups) + "," + last3


def amount_to_legal_format(amount: float) -> str:
    rupees = int(amount)
    paise = round((amount - rupees) * 100)

    formatted = format_indian_number(rupees)
    words = number_to_words_indian(rupees)

    if paise > 0:
        return f"Rs.{formatted}.{paise:02d}/- (Rupees {words} and {number_to_words_indian(paise)} Paise only)"
    return f"Rs.{formatted}/- (Rupees {words} only)"
