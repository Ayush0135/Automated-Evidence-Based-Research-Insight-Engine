## 2025-05-15 - Parallelizing Academic Scoring (Stage 4)
**Learning:** Sequential LLM calls in research pipelines are a major I/O bottleneck. Parallelizing Stage 4 with a ThreadPoolExecutor (3 workers) reduced mock execution time for 5 documents from 5.0s to 2.0s (2.5x speedup). Iterating over submitted futures ensures document order is preserved, which is critical for ranking-based stages.
**Action:** Always identify sequential LLM or network I/O loops and parallelize them using ThreadPoolExecutor while ensuring order preservation where required.
