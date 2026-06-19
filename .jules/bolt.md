## 2025-05-14 - Parallelizing LLM scoring calls
**Learning:** Stage 4 (Academic Scoring) was previously sequential, causing a bottleneck where each document added ~1-2 seconds of latency. Since LLM calls are I/O bound, parallelizing them with a ThreadPoolExecutor provides a linear speedup relative to the number of workers, until hitting rate limits.
**Action:** Always check for sequential loops containing network requests (LLM, Search, Scraping) and apply ThreadPoolExecutor with a conservative worker count (3-5) to balance speed and rate-limit safety.

## 2026-06-19 - Connection Pooling for Search and Discovery
**Learning:** The pipeline performs numerous repeated HTTP requests to the same hosts (Google Search API and various document sources). Without a session, each request incurs a full TCP/TLS handshake. Using a global `requests.Session` with an `HTTPAdapter` (pool_maxsize=20) allows connection reuse, significantly reducing latency.
**Action:** Always use connection pooling for modules that perform high-volume or repeated external requests. Benchmark showed ~40% improvement in throughput for repeated requests.
