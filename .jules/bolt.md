## 2025-05-15 - [Preserving Order in Parallelized Pipelines]
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` is a performance anti-pattern for this research pipeline because it scrambles document relevance (Stage 2) and text chunk chronology (Stage 3), which degrades the quality of synthesis.
**Action:** Always gather results by iterating over the list of futures in submission order when the sequence of items represents relevance or logical flow.
