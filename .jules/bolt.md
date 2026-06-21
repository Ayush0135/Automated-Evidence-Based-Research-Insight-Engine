## 2025-05-14 - Parallelizing LLM scoring calls
**Learning:** Stage 4 (Academic Scoring) was previously sequential, causing a bottleneck where each document added ~1-2 seconds of latency. Since LLM calls are I/O bound, parallelizing them with a ThreadPoolExecutor provides a linear speedup relative to the number of workers, until hitting rate limits.
**Action:** Always check for sequential loops containing network requests (LLM, Search, Scraping) and apply ThreadPoolExecutor with a conservative worker count (3-5) to balance speed and rate-limit safety.

## 2025-05-15 - Connection Pooling in Search Utilities
**Learning:** Benchmarking 10 concurrent requests to a stable endpoint (Google) showed a ~41% reduction in latency when using a global `requests.Session` compared to individual `requests.get` calls. This is due to reusing TCP/TLS connections, which is particularly beneficial when Stage 2 downloads multiple documents in parallel.
**Action:** Always implement connection pooling for high-volume network requests in the pipeline to avoid redundant handshake overhead.
