## 2026-06-06 - Parallelizing Academic Scoring
**Learning:** Sequential LLM API calls in Stage 4 were a major bottleneck, especially when processing many documents. Parallelizing with ThreadPoolExecutor (3 workers) achieved a 2.5x speedup in benchmarks without hitting rate limits.
**Action:** Always check for sequential API calls in pipeline stages and parallelize them using a conservative worker count to balance speed and provider limits.
