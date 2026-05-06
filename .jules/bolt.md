## 2025-05-14 - Parallelizing I/O Bound LLM Calls
**Learning:** Sequential LLM calls in research pipelines are a major I/O bottleneck. Parallelizing these calls using `ThreadPoolExecutor` significantly improves throughput without much complexity.
**Action:** Always check if LLM calls in loops can be parallelized. Use `ThreadPoolExecutor` and iterate over submitted futures to preserve document ranking/order.
