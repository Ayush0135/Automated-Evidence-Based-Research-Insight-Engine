
import requests
import time
import os
from bs4 import BeautifulSoup
import io
import PyPDF2

def download_and_parse_session(url, session):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '').lower()

        if 'application/pdf' in content_type or url.endswith('.pdf'):
            try:
                with io.BytesIO(response.content) as open_pdf_file:
                    reader = PyPDF2.PdfReader(open_pdf_file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except Exception as e:
                return ""
        else:
            soup = BeautifulSoup(response.content, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
    except Exception as e:
        return ""

def benchmark_with_session():
    urls = [
        "https://www.google.com",
        "https://www.wikipedia.org",
        "https://www.github.com",
        "https://www.python.org",
        "https://www.bing.com"
    ]

    session = requests.Session()
    start_time = time.time()
    for url in urls:
        download_and_parse_session(url, session)
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    print("Measuring performance with session...")
    duration = benchmark_with_session()
    print(f"Total time for 5 requests with session: {duration:.4f} seconds")
