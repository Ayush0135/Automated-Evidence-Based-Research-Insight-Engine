
import requests
import time

def benchmark_no_session(url, count=5):
    start_time = time.time()
    for _ in range(count):
        try:
            requests.get(url, timeout=10)
        except:
            pass
    return time.time() - start_time

def benchmark_with_session(url, count=5):
    session = requests.Session()
    start_time = time.time()
    for _ in range(count):
        try:
            session.get(url, timeout=10)
        except:
            pass
    return time.time() - start_time

if __name__ == "__main__":
    url = "https://www.google.com"
    print(f"Benchmarking {url}...")
    t1 = benchmark_no_session(url)
    print(f"No session: {t1:.4f}s")
    t2 = benchmark_with_session(url)
    print(f"With session: {t2:.4f}s")
    print(f"Improvement: {(t1-t2)/t1*100:.2f}%")
