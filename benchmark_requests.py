
import requests
import time
import os
from utils.search import google_search, download_and_parse

def benchmark_no_session():
    urls = [
        "https://www.google.com",
        "https://www.wikipedia.org",
        "https://www.github.com",
        "https://www.python.org",
        "https://www.bing.com"
    ]

    start_time = time.time()
    for url in urls:
        try:
            # We use download_and_parse which currently uses requests.get
            download_and_parse(url)
        except:
            pass
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    print("Measuring baseline performance (no session)...")
    duration = benchmark_no_session()
    print(f"Total time for 5 requests: {duration:.4f} seconds")
