import argparse
import logging
import pandas as pd
from Bio import Entrez
import time
import re


Entrez.email = "soumyapratapsingh.work@gmail.com" 

def setup_logging(debug):
         """Configure logging based on debug flag."""
         level = logging.DEBUG if debug else logging.INFO
         logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_papers(query, email, api_key=None, max_results=100):
         """Fetch papers from PubMed using the provided query."""
         Entrez.email = email
         if api_key:
             Entrez.api_key = api_key
         try:
             logging.debug(f"Executing search with query: {query}")
             handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
             record = Entrez.read(handle)
             handle.close()
             return record["IdList"]
         except Exception as e:
             logging.error(f"Error fetching papers: {e}")
             return []

def get_paper_details(pmid):
         """Retrieve details for a specific PubMed ID."""
         time.sleep(0.34)  # Rate limit: ~3 requests/second without API key
         try:
             logging.debug(f"Fetching details for PMID: {pmid}")
             handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
             record = Entrez.read(handle)
             handle.close()
             
             article = record["PubmedArticle"][0]["MedlineCitation"]["Article"]
             title = article.get("ArticleTitle", "N/A")
             
             pub_date = "N/A"
             if article.get("Journal", {}).get("JournalIssue", {}).get("PubDate"):
                 date_dict = article["Journal"]["JournalIssue"]["PubDate"]
                 pub_date = f"{date_dict.get('Year', 'N/A')}-{date_dict.get('Month', 'N/A')}-{date_dict.get('Day', 'N/A')}"
             
             authors = article.get("AuthorList", [])
             email = "N/A"
             affiliation = "N/A"
             for author in authors:
                 if author.get("AffiliationInfo"):
                     aff = author["AffiliationInfo"][0].get("Affiliation", "N/A")
                     if is_pharma_biotech(aff):
                         affiliation = aff
                         email = author["AffiliationInfo"][0].get("Email", "N/A") if "Email" in author["AffiliationInfo"][0] else "N/A"
                         if email == "N/A":
                             logging.debug(f"No email found for PMID {pmid}")
                         break
             
             return {
                 "PMID": pmid,
                 "Title": title,
                 "Publication Date": pub_date,
                 "Corresponding Author Email": email,
                 "Affiliation": affiliation
             }
         except Exception as e:
             logging.error(f"Error fetching details for PMID {pmid}: {e}")
             return None

def is_pharma_biotech(affiliation):
         """Check if affiliation indicates a pharmaceutical or biotech company."""
         pharma_keywords = [r"\bInc\b", r"\bLtd\b", r"\bPharma\b", r"\bBiotech\b", r"\bLaboratories\b", r"\bPharmaceuticals\b"]
         return any(re.search(keyword, affiliation, re.IGNORECASE) for keyword in pharma_keywords)

def main():
         parser = argparse.ArgumentParser(description="Fetch research papers from PubMed with pharmaceutical/biotech affiliations.")
         parser.add_argument("--query", required=True, help="Search query for PubMed (e.g., 'biotech cancer')")
         parser.add_argument("--email", default=Entrez.email, help="Email address for PubMed API access (default from code)")
         parser.add_argument("--api-key", default=None, help="NCBI API key for higher rate limits (optional)")
         parser.add_argument("--output", default="papers.csv", help="Output CSV filename (default: papers.csv)")
         parser.add_argument("--max-results", type=int, default=100, help="Maximum number of results to fetch (default: 100)")
         parser.add_argument("--debug", action="store_true", help="Enable debug logging")
         
         args = parser.parse_args()
         setup_logging(args.debug)
         
         logging.info("Starting paper fetch process")
         pmids = fetch_papers(args.query, args.email, args.api_key, args.max_results)
         
         if not pmids:
             logging.warning("No papers found for the query.")
             return
         
         papers = []
         for pmid in pmids:
             paper = get_paper_details(pmid)
             if paper and paper["Affiliation"] != "N/A":
                 papers.append(paper)
             else:
                 logging.debug(f"Skipping PMID {pmid} due to no pharma/biotech affiliation")
         
         if papers:
             df = pd.DataFrame(papers)
             df.to_csv(args.output, index=False)
             logging.info(f"Saved {len(papers)} papers to {args.output}")
         else:
             logging.warning("No papers with pharmaceutical/biotech affiliations found.")

if __name__ == "__main__":
         main()
