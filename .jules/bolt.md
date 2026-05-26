## 2025-05-14 - Parallel LLM Scoring & Connection Pooling
**Learning:** Sequential LLM calls in research pipelines are the primary bottleneck. Parallelizing Stage 4 with 3 workers reduced mock execution time from 5s to 2s (~60% reduction). Connection pooling via `requests.Session` provides an additional ~35-45% speedup for discovery stages by reusing TCP connections for searches and downloads.
**Action:** Always prefer `ThreadPoolExecutor` for stages involving multiple independent LLM calls and use a global `requests.Session` for network-heavy utilities.
