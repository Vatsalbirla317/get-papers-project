import logging
from typing import Generator

# This is the correct way to import sibling modules within a package
from . import api, parser, identifier
from .models import Paper

def process_paper(paper: Paper) -> bool:
    """
    Processes a single paper to find non-academic authors and affiliations.
    Returns True if the paper has at least one company affiliation, False otherwise.
    """
    has_company_affiliation = False
    
    # Find corresponding author email (does this once per paper)
    paper.find_corresponding_email()
    
    # Identify non-academic authors and their affiliations
    company_authors = set()
    company_affs = set()

    for author in paper.authors:
        company = identifier.get_company_affiliation(author.affiliation)
        if company:
            has_company_affiliation = True
            if author.full_name:
                company_authors.add(author.full_name)
            company_affs.add(company)
    
    if has_company_affiliation:
        paper.non_academic_authors = sorted(list(company_authors))
        paper.company_affiliations = sorted(list(company_affs))

    return has_company_affiliation


def find_papers(query: str) -> Generator[Paper, None, None]:
    """
    Main logic: searches PubMed, fetches details, parses, filters, and yields papers
    that have at least one author with a company affiliation.
    """
    pmids = api.search_pubmed(query)
    if not pmids:
        logging.warning("No papers found for the query.")
        return

    # Fetch in batches to be nice to the API
    batch_size = 100
    for i in range(0, len(pmids), batch_size):
        batch_pmids = pmids[i:i+batch_size]
        xml_data = api.fetch_paper_details(batch_pmids)
        if not xml_data:
            continue
        
        papers = parser.parse_pubmed_xml(xml_data)

        for paper in papers:
            if process_paper(paper):
                yield paper