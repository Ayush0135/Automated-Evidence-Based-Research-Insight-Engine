## 2025-05-23 - Parallelizing I/O-bound LLM Stages
**Learning:** Sequential LLM API calls in the research pipeline (like Stage 4 Academic Scoring) represent a major I/O bottleneck. Parallelizing these calls using `ThreadPoolExecutor` can achieve significant speedups (e.g., 2.5x with 3 workers) without compromising document order if futures are collected in submission order.
**Action:** Identify other sequential LLM processing stages and apply similar parallelization patterns while balancing rate limits with `max_workers`.
