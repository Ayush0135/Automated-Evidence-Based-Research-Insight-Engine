## 2025-05-22 - [Parallelized Stage 4 Academic Scoring]
**Learning:** Sequential LLM API calls in research pipelines are major I/O bottlenecks. In Stage 4, scoring 10 documents took 5.0s because each call waited for the previous one. Parallelizing with `ThreadPoolExecutor` while iterating over submitted futures allowed for a 2.5x speedup (with 3 workers) without losing the relevance-based ranking established in earlier stages.
**Action:** Always identify sequential LLM/API call loops and apply parallelization with order preservation using the `futures` list iteration pattern.
