## 2025-05-14 - Parallelizing LLM scoring calls
**Learning:** Stage 4 (Academic Scoring) was previously sequential, causing a bottleneck where each document added ~1-2 seconds of latency. Since LLM calls are I/O bound, parallelizing them with a ThreadPoolExecutor provides a linear speedup relative to the number of workers, until hitting rate limits.
**Action:** Always check for sequential loops containing network requests (LLM, Search, Scraping) and apply ThreadPoolExecutor with a conservative worker count (3-5) to balance speed and rate-limit safety.

## 2025-05-15 - HTTP Connection Pooling
**Learning:** Initializing a global `requests.Session` with an `HTTPAdapter` (pooling) significantly reduces latency for network-heavy applications. Benchmarking showed a ~41% reduction in response time (from ~0.91s to ~0.54s for 10 requests) by reusing TCP/TLS connections.
**Action:** In any module performing multiple external API calls or scraping (e.g., Search, Discovery), always prefer a shared `requests.Session` over individual `requests.get/post` calls to leverage connection reuse.

## 2025-05-16 - Centralized Regex & Model Re-use
**Learning:** Pre-compiling regex patterns (`re.compile`) and centralizing extraction logic reduces repeated parsing overhead and ensures consistency across a multi-stage pipeline. Additionally, reusing LLM model instances (like Gemini's `GenerativeModel`) at the module level avoids redundant object instantiation, even if lightweight.
**Action:** Always pre-compile frequently used regex patterns and centralize common parsing utilities. Move LLM model initialization outside of hot-path functions to the module level where possible.
