import os
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import io
import PyPDF2
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Initialize a global session for connection pooling
# This significantly improves performance by reusing TCP/TLS connections
session = requests.Session()
# Set default headers on the session to avoid redundant dictionary creation in every request
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})
adapter = HTTPAdapter(pool_connections=20, pool_maxsize=20)
session.mount("http://", adapter)
session.mount("https://", adapter)

def google_search(query, num_results=5):
    """
    Performs a Google Custom Search.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CSE_ID,
        'q': query,
        'num': num_results
    }
    try:
        # Added timeout for robustness
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get('items', [])
    except Exception as e:
        print(f"Error performing Google Search: {e}")
        return []

def download_and_parse(url):
    """
    Downloads content from a URL and extracts text.
    Handles HTML and basic PDF parsing.
    """
    try:
        # headers already set on session
        response = session.get(url, timeout=10)
        response.raise_for_status()
        
        content_type = response.headers.get('Content-Type', '').lower()
        
        if 'application/pdf' in content_type or url.endswith('.pdf'):
            try:
                with io.BytesIO(response.content) as open_pdf_file:
                    reader = PyPDF2.PdfReader(open_pdf_file)
                    # Use "".join for more efficient string synthesis
                    return "\n".join(filter(None, (page.extract_text() for page in reader.pages)))
            except Exception as e:
                print(f"Error parsing PDF {url}: {e}")
                return ""
        else:
            # Assume HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            # Kill all script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            # Break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text

    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return ""
