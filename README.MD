# Get Papers

A command-line tool to fetch research papers from PubMed based on a user-specified query. The program filters for papers that have at least one author affiliated with a pharmaceutical or biotech company.

## Features

-   Fetches data directly from the PubMed API.
-   Supports PubMed's full query syntax.
-   Filters papers to include only those with authors from pharma/biotech companies.
-   Outputs results to a CSV file or to the console.
-   Configurable logging for debugging.

## Code Organization

The project is structured into two main parts: a core library and a command-line interface (CLI).

-   `get_papers/`: This is the core Python package/module.
    -   `api.py`: Handles all communication with the PubMed API (searching and fetching).
    -   `parser.py`: Parses the XML data returned by the API into structured Python objects.
    -   `identifier.py`: Contains the heuristic logic to determine if an author's affiliation is a company.
    -   `models.py`: Defines the Pydantic data models (`Paper`, `Author`) for type safety and validation.
    -   `core.py`: Orchestrates the process by calling the other modules to find and filter papers.
-   `cli.py`: A thin wrapper around the `get_papers` library. It uses `Typer` to handle command-line arguments and manages I/O (writing the final CSV file or printing to the console).

This separation of concerns makes the core logic reusable and easier to test independently of the command-line interface.

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging.

1.  **Clone the repository (or create the files as provided):**
    ```bash
    git clone <your-github-repo-url>
    cd get-papers-project
    ```

2.  **Install dependencies:**
    Ensure you have Poetry installed. Then, run from the project's root directory:
    ```bash
    poetry install
    ```
    This command reads the `pyproject.toml` file, creates a virtual environment, and installs all the necessary libraries.

## Execution

You can run the program using `poetry run`. The main command is `get-papers-list`.

### Syntax

```bash
poetry run get-papers-list "YOUR_PUBMED_QUERY" [OPTIONS]