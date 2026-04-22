## 2026-04-22 - Parallelizing I/O-bound LLM Stages
**Learning:** Sequential LLM API calls in research pipelines create significant latency. Parallelizing these calls using `ThreadPoolExecutor` provides a linear speedup (up to worker count) without impacting the logic of independent document processing.
**Action:** Always identify independent I/O tasks (like document scoring or discovery) and parallelize them early, ensuring result order is preserved by iterating over futures in submission order.
