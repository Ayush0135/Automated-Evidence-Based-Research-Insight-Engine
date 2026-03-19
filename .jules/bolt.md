## 2025-05-22 - Identifying Serial Execution Bottleneck in Stage 4
**Learning:** Stage 4 (Academic Scoring) processes documents sequentially, which becomes a bottleneck when dealing with multiple sources. Since scoring each document is an independent I/O-bound LLM call, it is highly suitable for parallelization.
**Action:** Parallelize Stage 4 using ThreadPoolExecutor while maintaining document order.
