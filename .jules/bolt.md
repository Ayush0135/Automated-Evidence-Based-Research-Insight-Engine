## 2025-05-15 - Order Preservation in Parallel Stages
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` for LLM tasks (Stages 2, 3, and 4) scrambles result order, which can degrade quality if relevance or chronology matters.
**Action:** Always iterate over futures in submission order when gathering results in parallelized research stages to preserve input sequence.
