## 2025-05-14 - Parallelizing Stage 4 Scoring
**Learning:** Sequential LLM calls in research pipelines are a major I/O bottleneck. Parallelizing with `ThreadPoolExecutor` and a conservative `max_workers` (e.g., 3) provides a significant speedup (up to 2.5x for 10 docs) without exceeding typical rate limits.
**Action:** Always look for sequential loops containing I/O (LLM calls, network requests) and parallelize them while ensuring result order is preserved by iterating over submitted futures.
