## 2025-05-14 - Parallelizing Stage 4 Academic Scoring
**Learning:** Sequential LLM scoring calls in Stage 4 created a significant bottleneck. Parallelizing with `ThreadPoolExecutor` and a conservative `max_workers=3` (to balance speed and rate limits) reduced execution time from 5.00s to 2.00s for 5 documents in benchmarks, achieving a 2.5x speedup.
**Action:** Systematically identify sequential I/O-bound LLM or API calls in pipeline stages and apply parallelization with `ThreadPoolExecutor` and `as_completed` for immediate performance gains.
