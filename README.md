PubMed Paper Fetcher
 A Python tool to fetch research papers from PubMed, filter for pharmaceutical/biotech affiliations, and save results to a CSV file.

 ## Installation

 1. Install Poetry:
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
 2. Clone the repository or create a project:
    ```bash
    git clone 
    cd pubmed-fetcher
    poetry install
    ```
 3. Activate the virtual environment:
    ```bash
    poetry shell
    ```

 ## Dependencies

 - `biopython`: For PubMed API access
 - `pandas`: For CSV handling
 - `requests`: For HTTP requests

 ## Usage

 Run the script with the following command:
 ```bash
 poetry run get-papers-list --query "biotech cancer" --email "your.email@example.com" --output results.csv --max-results 100 --debug
 ```

 ### Options

 - `--query`: PubMed search query (required)
 - `--email`: Your email for PubMed API access (required)
 - `--api-key`: NCBI API key for higher rate limits (optional)
 - `--output`: Output CSV filename (default: `papers.csv`)
 - `--max-results`: Maximum number of results to fetch (default: 100)
 - `--debug`: Enable detailed debug logging

 ## Output

 The output CSV contains:
 - `PMID`: PubMed unique identifier
 - `Title`: Paper title
 - `Publication Date`: Publication date (YYYY-MM-DD)
 - `Corresponding Author Email`: Email of the corresponding author (if available)
 - `Affiliation`: Pharmaceutical/biotech affiliation

 ## Example

 ```bash
 poetry run get-papers-list --query "pharma vaccine" --email "user@example.com" --api-key "your_api_key" --output vaccines.csv
 ```

 ## Notes

 - Ensure a valid email is provided for PubMed API compliance.
 - An API key (from [NCBI](https://www.ncbi.nlm.nih.gov/account/)) is optional but recommended for large queries.
 - Debug mode (`--debug`) provides detailed logs.
 - Emails are rarely available in PubMed data.

 ## Code Organization

 - `pubmed_fetcher/`: Package containing `get_papers_list.py`.
 - `pyproject.toml`: Project configuration and dependencies.
 - `README.md`: This documentation.

 ## GitHub Repository

 [https://github.com/SOUMYAPRATAPSINGH/Aganith---Python-Take-Home-Exercise](https://github.com/SOUMYAPRATAPSINGH/Aganith---Python-Take-Home-Exercise)  

 ## Issues

 Report issues on the GitHub repository.
