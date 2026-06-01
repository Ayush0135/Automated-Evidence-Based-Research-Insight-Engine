## 2025-05-15 - Parallelizing Stage 4 Academic Scoring
**Learning:** Network-bound LLM calls in sequential loops are a primary bottleneck. Parallelizing them with `ThreadPoolExecutor` and a conservative `max_workers` (e.g., 3) provides significant speedups (2.5x in this case) without risking aggressive rate limits.
**Action:** Always look for sequential I/O or API calls in stages and apply parallelization patterns where order can be preserved via future tracking.
