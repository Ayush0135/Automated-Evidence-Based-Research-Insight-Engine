## 2025-05-15 - Stage 4 Parallelization Speedup
**Learning:** Parallelizing the academic scoring stage (Stage 4) using `ThreadPoolExecutor` with 3 workers reduced the mock execution time for 5 documents from 5.00s to 2.00s, a 2.5x speedup. This confirms that I/O-bound LLM scoring is a major bottleneck that benefits significantly from concurrency without sacrificing code readability.
**Action:** Always identify sequential LLM API calls in pipeline stages and apply parallel processing using `ThreadPoolExecutor` with a conservative worker count to stay within rate limits.
