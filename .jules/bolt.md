## 2025-05-15 - Order Preservation in Parallel Pipelines
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in research pipelines is a performance anti-pattern when input order (relevance ranking) must be preserved. While `as_completed()` returns results as they finish, it scrambles the document sequence, degrading the quality of downstream synthesis and filtering stages.
**Action:** Always iterate over futures in the order they were submitted (`for future in futures:`) when parallelizing pipeline stages that depend on input sequence or chronological order (like text chunks).
