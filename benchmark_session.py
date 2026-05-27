
import requests
import time
import statistics

def benchmark_requests(url, count=5):
    print(f"Benchmarking {url} ({count} requests)...")

    # Without Session
    durations_no_session = []
    for _ in range(count):
        start = time.time()
        r = requests.get(url)
        durations_no_session.append(time.time() - start)
        r.close()

    avg_no_session = statistics.mean(durations_no_session)
    print(f"Average without Session: {avg_no_session:.4f}s")

    # With Session
    durations_session = []
    session = requests.Session()
    for _ in range(count):
        start = time.time()
        r = session.get(url)
        durations_session.append(time.time() - start)
        r.close()

    avg_session = statistics.mean(durations_session)
    print(f"Average with Session: {avg_session:.4f}s")

    improvement = (avg_no_session - avg_session) / avg_no_session * 100
    print(f"Improvement: {improvement:.2f}%")

if __name__ == "__main__":
    # Using a reliable fast URL
    benchmark_requests("https://www.google.com", count=10)
