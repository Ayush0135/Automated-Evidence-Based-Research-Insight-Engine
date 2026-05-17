## 2026-05-17 - [Parallelization of Stage 4 Scoring]
**Learning:** Sequential LLM calls in research pipelines are I/O bottlenecks. Parallelizing these with ThreadPoolExecutor and preserving order by iterating over submitted futures significantly improves throughput (2.5x speedup for 10 docs with 3 workers).
**Action:** Always identify sequential LLM loops and consider ThreadPoolExecutor for concurrent processing while ensuring order preservation where relevance matters.
