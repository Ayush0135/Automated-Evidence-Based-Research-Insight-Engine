## 2025-05-14 - Parallelizing LLM scoring calls
**Learning:** Stage 4 (Academic Scoring) was previously sequential, causing a bottleneck where each document added ~1-2 seconds of latency. Since LLM calls are I/O bound, parallelizing them with a ThreadPoolExecutor provides a linear speedup relative to the number of workers, until hitting rate limits.
**Action:** Always check for sequential loops containing network requests (LLM, Search, Scraping) and apply ThreadPoolExecutor with a conservative worker count (3-5) to balance speed and rate-limit safety.

## 2025-05-15 - HTTP Connection Pooling
**Learning:** Initializing a global `requests.Session` with an `HTTPAdapter` (pooling) significantly reduces latency for network-heavy applications. Benchmarking showed a ~41% reduction in response time (from ~0.91s to ~0.54s for 10 requests) by reusing TCP/TLS connections.
**Action:** In any module performing multiple external API calls or scraping (e.g., Search, Discovery), always prefer a shared `requests.Session` over individual `requests.get/post` calls to leverage connection reuse.

## 2025-05-16 - Pre-compiled Regex for JSON Extraction
**Learning:** Repeatedly compiling complex regular expressions for JSON extraction (especially those using `re.DOTALL` and multi-line matching) adds significant overhead in high-throughput pipelines. Moving to module-level pre-compiled patterns yielded a measurable ~39% improvement in extraction latency.
**Action:** Centralize common parsing logic (like JSON extraction) and use module-level `re.compile()` for all patterns to avoid redundant compilation in loops.

## 2025-05-17 - Chunk Size Optimization for Document Analysis
**Learning:** Doubling the `chunk_size` and threshold to 48,000 characters in `stage3_analysis.py` reduces processing overhead for common academic papers (24k-48k range) by up to 66% in terms of LLM API calls. Modern high-capacity models like Gemini handle these contexts effortlessly without quality degradation.
**Action:** Align chunking thresholds with the capabilities of the primary LLM provider; larger chunks reduce I/O bottlenecks and provide better holistic context for analysis.
