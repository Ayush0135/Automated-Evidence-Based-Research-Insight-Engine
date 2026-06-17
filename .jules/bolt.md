## 2025-05-14 - Parallelizing LLM scoring calls
**Learning:** Stage 4 (Academic Scoring) was previously sequential, causing a bottleneck where each document added ~1-2 seconds of latency. Since LLM calls are I/O bound, parallelizing them with a ThreadPoolExecutor provides a linear speedup relative to the number of workers, until hitting rate limits.
**Action:** Always check for sequential loops containing network requests (LLM, Search, Scraping) and apply ThreadPoolExecutor with a conservative worker count (3-5) to balance speed and rate-limit safety.

## 2025-05-15 - Connection Pooling for repeated HTTP requests
**Learning:** For utility modules that perform many HTTP requests to the same hosts (like search APIs or document providers), using a persistent `requests.Session()` instead of `requests.get()` reduces latency significantly by reusing TCP/TLS connections (HTTP Keep-Alive).
**Action:** Use `requests.Session()` at the module or class level for high-volume networking utilities to minimize handshake overhead.
