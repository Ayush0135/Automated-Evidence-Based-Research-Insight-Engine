## 2026-02-19 - Pipeline Concurrency Optimization
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in this codebase is a performance anti-pattern because it scrambles document relevance ranking and text chunk chronology, which degrades downstream synthesis quality.
**Action:** Always maintain input sequence order when using `ThreadPoolExecutor` by iterating over the list of futures in the order they were submitted.
