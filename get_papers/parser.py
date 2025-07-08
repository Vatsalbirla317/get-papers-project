import logging
from lxml import etree
from typing import List, Optional
from .models import Paper, Author

def _get_text(node, xpath_str: str) -> Optional[str]:
    """Safely get text from an XML node using XPath."""
    try:
        return node.xpath(xpath_str)[0].text
    except (IndexError, AttributeError):
        return None

def parse_paper_from_xml_node(article_node) -> Paper:
    """Parses a single <PubmedArticle> node into a Paper object."""
    pmid = _get_text(article_node, ".//MedlineCitation/PMID")
    title = _get_text(article_node, ".//ArticleTitle")

    # Publication date parsing
    pub_date_node = article_node.find(".//PubDate")
    if pub_date_node is not None:
        year = _get_text(pub_date_node, "Year")
        month = _get_text(pub_date_node, "Month")
        day = _get_text(pub_date_node, "Day")
        publication_date = f"{year or 'N/A'}-{month or 'N/A'}-{day or 'N/A'}"
    else:
        publication_date = "N/A"

    paper_data = {
        "PMID": pmid,
        "title": title,
        "publication_date": publication_date,
        "authors": []
    }

    # Author parsing
    author_nodes = article_node.xpath(".//AuthorList/Author")
    for author_node in author_nodes:
        affiliation_node = author_node.find(".//AffiliationInfo/Affiliation")
        author = Author(
            last_name=_get_text(author_node, "LastName"),
            fore_name=_get_text(author_node, "ForeName"),
            initials=_get_text(author_node, "Initials"),
            affiliation=affiliation_node.text if affiliation_node is not None else None
        )
        paper_data["authors"].append(author)

    return Paper.parse_obj(paper_data)

def parse_pubmed_xml(xml_data: str) -> List[Paper]:
    """Parses the entire XML string from an efetch result."""
    if not xml_data:
        return []
    
    try:
        # We need to handle potential encoding issues
        root = etree.fromstring(xml_data.encode('utf-8'))
        papers = [parse_paper_from_xml_node(article) for article in root.xpath("//PubmedArticle")]
        logging.info(f"Successfully parsed {len(papers)} papers from XML.")
        return papers
    except etree.XMLSyntaxError as e:
        logging.error(f"Failed to parse XML: {e}")
        return []