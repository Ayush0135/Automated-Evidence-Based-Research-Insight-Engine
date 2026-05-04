## 2025-05-15 - Parallelizing Sequential LLM Stages
**Learning:** Sequential LLM calls in research pipelines are massive I/O bottlenecks. Stage 4 was processing documents one-by-one, leading to linear scaling of latency. Parallelizing with a small worker pool (3 workers) achieved a 2.5x speedup without hitting rate limits.
**Action:** Always check for sequential loops containing `query_llm` or similar network-bound calls and parallelize them using `ThreadPoolExecutor` while ensuring output order is preserved by iterating over the submission-ordered futures list.
