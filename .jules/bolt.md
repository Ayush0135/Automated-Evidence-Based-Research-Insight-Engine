## 2025-01-24 - Stage 4 Parallelization and Order Preservation
**Learning:** Sequential LLM API calls in Stage 4 were a major bottleneck. However, using `as_completed()` with `ThreadPoolExecutor` is a performance anti-pattern here because it scrambles document relevance, which downstream stages (like Stage 5 filtering) depend on.
**Action:** Always iterate over the list of futures in submission order when gathering results from `ThreadPoolExecutor` to preserve input sequence while gaining parallel throughput.
