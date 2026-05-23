
import requests
import time
from utils.search import google_search

def benchmark_requests():
    print("Benchmarking requests.get vs requests.Session()...")
    url = "https://www.google.com"

    # Test requests.get
    start = time.time()
    for _ in range(10):
        requests.get(url)
    end = time.time()
    print(f"requests.get: {end - start:.4f}s")

    # Test requests.Session()
    session = requests.Session()
    start = time.time()
    for _ in range(10):
        session.get(url)
    end = time.time()
    print(f"requests.Session: {end - start:.4f}s")

if __name__ == "__main__":
    benchmark_requests()
