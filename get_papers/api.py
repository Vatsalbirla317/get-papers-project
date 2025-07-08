# get_papers/api.py
import logging
import requests
from typing import List

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
# For higher rate limits, get a free API key from your NCBI account
# and set it as an environment variable or here directly.
API_KEY = None

def search_pubmed(query: str, max_results: int = 200) -> List[str]:
    """Search PubMed and return a list of PubMed IDs (PMIDs)."""
    logging.info(f"Searching PubMed with query: '{query}'")
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "usehistory": "y",
        "retmode": "json",
    }
    if API_KEY:
        params["api_key"] = API_KEY

    try:
        response = requests.get(f"{BASE_URL}esearch.fcgi", params=params)
        response.raise_for_status()
        data = response.json()
        pmids = data.get("esearchresult", {}).get("idlist", [])
        logging.info(f"Found {len(pmids)} PMIDs.")
        return pmids
    except requests.RequestException as e:
        logging.error(f"API search request failed: {e}")
        return []

def fetch_paper_details(pmids: List[str]) -> str:
    """Fetch full paper details for a list of PMIDs in XML format."""
    if not pmids:
        return ""
    logging.info(f"Fetching details for {len(pmids)} PMIDs.")

    # Using POST is better for long lists of IDs
    params = {
        "db": "pubmed",
        "retmode": "xml",
        "rettype": "abstract",
    }
    if API_KEY:
        params["api_key"] = API_KEY

    try:
        response = requests.post(f"{BASE_URL}efetch.fcgi", params=params, data={"id": ",".join(pmids)})
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"API fetch request failed: {e}")
        return ""