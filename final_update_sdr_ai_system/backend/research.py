import requests
from bs4 import BeautifulSoup
import re

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CUSTOM_SEARCH_CX = os.getenv("CUSTOM_SEARCH_CX")

def search_prospect_info(query: str):
    """
    Perform a Google Custom Search and return URLs from the search results.
    """
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={CUSTOM_SEARCH_CX}"
    response = requests.get(url)
    response.raise_for_status()
    search_results = response.json()

    urls = []
    if 'items' in search_results:
        for item in search_results['items']:
            url = item.get('link', '')
            return url
    else:
        raise ValueError("No search results found.")

def scrape_webpage(url: str):
    """
    Scrape text content from a webpage.
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])
    return text

def clean_content(content: str):
    # Regular expression pattern to match texts like [6], [5], [7], etc.
    cleaned_content = re.sub(r'\[\d+\]', '', content)
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()
    
    return cleaned_content

def generate_report(prospect_name: str, prospect_company_name: str):
    """
    Generate a report by searching for and scraping information about the prospect.
    """
    queries = [
        f"{prospect_name} {prospect_company_name}",
    ]

    all_texts = []
    for query in queries:
        url = search_prospect_info(query)
        text = scrape_webpage(url)
        cleaned_text = clean_content(text)
        all_texts.append(cleaned_text)
        combined_text = "\n".join(all_texts)
        return combined_text

    
