## 2025-05-14 - Order Preservation in Parallel Stages
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 is a performance anti-pattern in this codebase. While it might slightly reduce the time to the first result, it scrambles document relevance and text chunk chronology, which significantly degrades the quality of the final research synthesis.
**Action:** Always iterate over the list of futures in the order they were submitted to ensure results are processed and returned in their original, meaningful sequence.
