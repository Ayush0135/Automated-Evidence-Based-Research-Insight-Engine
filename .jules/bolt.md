## 2025-05-15 - Order Preservation in Parallel Stages
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 is a performance anti-pattern. While it allows processing results as they finish, it scrambles the document relevance order and text chunk chronology, which significantly degrades the quality of downstream synthesis and filtering.
**Action:** Always iterate over the list of futures in the order they were submitted to maintain sequence integrity during parallelization.
