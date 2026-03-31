## 2025-05-14 - ThreadPoolExecutor Order Anti-pattern
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 is a performance and quality anti-pattern in this codebase. While it allows processing as results arrive, it scrambles document relevance, query priority, and text chunk chronology, which significantly degrades the quality of the final research synthesis.
**Action:** Always iterate over the list of futures in the order they were submitted to maintain input sequence while benefiting from parallel throughput.
