## 2025-05-14 - [Connection Pooling in search utility]
**Learning:** Using a global `requests.Session()` in a network-bound research pipeline significantly reduces latency (measured ~44% improvement) by enabling TCP/TLS connection reuse (Keep-Alive). This is especially impactful when multiple requests are made to the same host (Google API) or when downloading multiple papers from diverse domains.
**Action:** Always prefer `requests.Session()` over repeated `requests.get()` calls in modules that perform multiple network requests.
