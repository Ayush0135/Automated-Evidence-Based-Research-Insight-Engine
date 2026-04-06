## 2025-01-24 - Parallelization Order Preservation
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` is a performance anti-pattern in this codebase because it scrambles document relevance and text chunk chronology, which degrades synthesis quality.
**Action:** Always gather results by iterating over the list of futures in the order they were submitted to maintain input sequence integrity.
