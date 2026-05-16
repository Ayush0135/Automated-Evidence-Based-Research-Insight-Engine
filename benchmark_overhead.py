
import time
import sys
import os
from unittest.mock import MagicMock

# Mocking dependencies
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
sys.modules['termcolor'] = MagicMock()
sys.modules['utils.llm_offline'] = MagicMock()
sys.modules['bs4'] = MagicMock()
sys.modules['PyPDF2'] = MagicMock()

import google.generativeai as genai
import requests
import utils.llm as llm
import utils.search as search

def benchmark_llm_caching():
    print("Benchmarking LLM caching impact...")

    # We want to see if calling _call_gemini multiple times avoids re-instantiation
    # Our optimized version uses the module level gemini_model

    # First, let's see how long it takes to instantiate a lot of times (simulated)
    start = time.perf_counter()
    for _ in range(1000):
        _ = genai.GenerativeModel('gemini-2.0-flash')
    end = time.perf_counter()
    instantiation_overhead = end - start
    print(f"Instantiation overhead for 1000 calls: {instantiation_overhead:.4f}s")

    # The optimized _call_gemini should now have near-zero instantiation overhead per call
    # since it uses the cached model.

def benchmark_import_overhead():
    print("\nBenchmarking import overhead...")
    # The optimization was moving 'from termcolor import colored' out of the loop
    # We can measure how much time is saved per 1000 "calls" that previously did the import

    def simulate_old_way():
        for _ in range(1000):
            from termcolor import colored
            _ = colored("test", "red")

    def simulate_new_way():
        from termcolor import colored
        for _ in range(1000):
            _ = colored("test", "red")

    start = time.perf_counter()
    simulate_old_way()
    end = time.perf_counter()
    old_time = end - start
    print(f"Old way (import in loop) 1000 times: {old_time:.4f}s")

    start = time.perf_counter()
    simulate_new_way()
    end = time.perf_counter()
    new_time = end - start
    print(f"New way (import outside) 1000 times: {new_time:.4f}s")
    print(f"Speedup: {old_time/new_time:.2f}x")

def verify_session_usage():
    print("\nVerifying session usage in utils/search.py...")
    if hasattr(search, 'session') and isinstance(search.session, requests.Session):
        print("SUCCESS: Global session object found and is a requests.Session instance.")
    else:
        print("FAILURE: Global session object not found or incorrect type.")

if __name__ == "__main__":
    benchmark_llm_caching()
    benchmark_import_overhead()
    verify_session_usage()
