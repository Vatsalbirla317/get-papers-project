from typing import Optional

# These lists can be expanded for better accuracy
COMPANY_KEYWORDS = ["inc", "ltd", "corp", "llc", "pharmaceuticals", "pharma", "biotech", "therapeutics", "diagnostics", "ventures"]
KNOWN_COMPANIES = ["pfizer", "novartis", "roche", "genentech", "merck", "gsk", "glaxosmithkline", "astrazeneca", "sanofi", "bayer", "amgen", "gilead", "regeneron", "moderna", "biontech"]
ACADEMIC_KEYWORDS = ["university", "college", "institute", "hospital", "school of medicine", "department of", "academy", "center for", "centre for", "medical center", "research council"]

def get_company_affiliation(affiliation_string: str) -> Optional[str]:
    """
    Checks if an affiliation is likely non-academic (a company).
    Returns the affiliation string if it's a company, otherwise None.
    """
    if not affiliation_string:
        return None

    lower_aff = affiliation_string.lower()

    # Rule 1: If it contains a common academic keyword, assume it's academic and reject it.
    if any(keyword in lower_aff for keyword in ACADEMIC_KEYWORDS):
        # Exception: Some company names contain "institute" (e.g., "Dana-Farber Cancer Institute" which has industry ties, but we'll keep it simple)
        # For this heuristic, we prioritize excluding academics.
        return None
        
    # Rule 2: If it contains a known company name or a company keyword, it's likely a company.
    if any(company in lower_aff for company in KNOWN_COMPANIES) or \
       any(keyword in lower_aff for keyword in COMPANY_KEYWORDS):
        return affiliation_string

    # Rule 3: As a fallback, if it doesn't have academic keywords but also doesn't have company keywords,
    # we can't be sure, so we reject it to reduce false positives.
    return None