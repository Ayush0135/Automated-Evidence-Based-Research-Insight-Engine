## 2025-05-14 - Parallelism Anti-pattern in Research Pipeline
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 scrambles document relevance and text chunk chronology. This degrades the quality of research synthesis as downstream stages rely on the original ranking and sequence.
**Action:** Always gather results by iterating over futures in their submission order to maintain sequence integrity during parallel operations.
