## 2025-05-14 - Parallelizing Academic Scoring Stage
**Learning:** Sequential LLM API calls in Stage 4 were a major bottleneck. Parallelizing them with `ThreadPoolExecutor` (3 workers) provided a 2.5x speedup (5.0s down to 2.0s for 5 documents) without hitting rate limits. Using `as_completed` allowed for faster overall completion while preserving the ability to collect all successful results.
**Action:** Apply similar `ThreadPoolExecutor` patterns to other I/O-bound or LLM-heavy stages (like Stage 3 chunk analysis) to further reduce pipeline latency.
