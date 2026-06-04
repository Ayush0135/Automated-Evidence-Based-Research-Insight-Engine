## 2025-05-14 - Parallelizing I/O-bound LLM scoring
**Learning:** Sequential LLM calls in a pipeline stage create a significant bottleneck that scales linearly with the number of documents. Using `ThreadPoolExecutor` even with a conservative worker count (e.g., 3) provides immediate and measurable speedups (~2.5x in this case) for I/O-bound tasks like API-based scoring.
**Action:** Always check if list processing involving LLM calls is parallelized in new or existing pipeline stages.
