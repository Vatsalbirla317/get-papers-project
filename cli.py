import sys
import csv
import logging
import typer
from typing_extensions import Annotated
from get_papers import core

app = typer.Typer(help="A tool to fetch pharma/biotech research papers from PubMed.")

def setup_logging(debug: bool):
    """Configure logging based on the debug flag."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

@app.command()
def main(
    query: Annotated[str, typer.Argument(help="The full PubMed query string.")],
    file: Annotated[str, typer.Option("--file", "-f", help="Path to save the output CSV file. Prints to console if not provided.")] = None,
    debug: Annotated[bool, typer.Option("--debug", "-d", help="Enable debug-level logging.")] = False
):
    """
    Fetch research papers from PubMed based on a query and filter for those with
    authors from pharmaceutical or biotech companies.
    """
    setup_logging(debug)
    
    try:
        results = list(core.find_papers(query))
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise typer.Exit(code=1)

    if not results:
        logging.info("No matching papers with company affiliations were found.")
        return

    logging.info(f"Found {len(results)} papers with company affiliations. Preparing output.")
    
    # Define output stream (file or stdout)
    output_stream = open(file, 'w', newline='', encoding='utf-8') if file else sys.stdout
    
    writer = csv.writer(output_stream)
    # Write header
    writer.writerow([
        "PubmedID", "Title", "Publication Date", 
        "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"
    ])
    
    # Write data rows
    for paper in results:
        writer.writerow([
            paper.pubmed_id,
            paper.title,
            paper.publication_date,
            "; ".join(paper.non_academic_authors),
            "; ".join(paper.company_affiliations),
            paper.corresponding_author_email or "N/A"
        ])

    if file:
        output_stream.close()
        typer.echo(f"Results successfully saved to {file}")

if __name__ == "__main__":
    app()