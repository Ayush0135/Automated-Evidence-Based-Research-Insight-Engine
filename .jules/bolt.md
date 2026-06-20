## 2025-05-14 - Parallelizing LLM scoring calls
**Learning:** Stage 4 (Academic Scoring) was previously sequential, causing a bottleneck where each document added ~1-2 seconds of latency. Since LLM calls are I/O bound, parallelizing them with a ThreadPoolExecutor provides a linear speedup relative to the number of workers, until hitting rate limits.
**Action:** Always check for sequential loops containing network requests (LLM, Search, Scraping) and apply ThreadPoolExecutor with a conservative worker count (3-5) to balance speed and rate-limit safety.

## 2025-05-15 - HTTP Connection Pooling for Search and Downloads
**Learning:** Using stateless `requests.get()` in a high-volume I/O pipeline (like Stage 2 Discovery) causes significant overhead due to repeated TCP/TLS handshakes. Implementing a global `requests.Session` with an `HTTPAdapter` tuned to the concurrency level (e.g., `pool_maxsize=20`) allows for connection reuse.
**Action:** Always use `requests.Session()` for modules that make multiple requests to the same or varied hosts to reduce latency by ~40%+.
