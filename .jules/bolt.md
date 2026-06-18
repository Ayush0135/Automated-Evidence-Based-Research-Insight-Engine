## 2025-05-14 - Parallelizing LLM scoring calls
**Learning:** Stage 4 (Academic Scoring) was previously sequential, causing a bottleneck where each document added ~1-2 seconds of latency. Since LLM calls are I/O bound, parallelizing them with a ThreadPoolExecutor provides a linear speedup relative to the number of workers, until hitting rate limits.
**Action:** Always check for sequential loops containing network requests (LLM, Search, Scraping) and apply ThreadPoolExecutor with a conservative worker count (3-5) to balance speed and rate-limit safety.

## 2026-06-18 - Connection Pooling with requests.Session
**Learning:** Reusing TCP connections via a global `requests.Session` significantly reduces latency in high-volume I/O tasks like document discovery. The TLS handshake overhead for multiple hosts (Google Search + various document sources) was a major bottleneck in the parallel execution of Stage 2.
**Action:** Always implement connection pooling using `requests.Session` and `HTTPAdapter` (for increased pool size) in utility modules that handle frequent network requests, especially when those requests are executed in parallel via `ThreadPoolExecutor`.
