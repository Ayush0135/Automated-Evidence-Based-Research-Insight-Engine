## 2025-05-22 - [Parallelization of Stage 4 Scoring]
**Learning:** Stage 4 (Academic Scoring) was a major sequential bottleneck in the research pipeline. Parallelizing it with `ThreadPoolExecutor` and a conservative `max_workers=3` (to avoid rate limits) achieved a 2.5x speedup in benchmarks (5.00s -> 2.00s for 5 documents).
**Action:** Always look for I/O-bound sequential loops (like LLM calls or downloads) and parallelize them with conservative worker counts to respect provider limits.
