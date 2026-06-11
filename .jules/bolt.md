## 2026-06-11 - Parallelizing Stage 4 Scoring
**Learning:** Stage 4 (Scoring) was a sequential bottleneck in the research pipeline. Parallelizing I/O-bound LLM calls with a conservative ThreadPoolExecutor (3 workers) achieved a ~2.5x speedup without exceeding typical API rate limits.
**Action:** Audit pipeline stages for sequential I/O-bound tasks and apply parallelization patterns where order preservation is maintained via future collection.
