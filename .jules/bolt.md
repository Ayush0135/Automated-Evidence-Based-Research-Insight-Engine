## 2024-04-24 - Order-Preserving Parallelism in Stage 4
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` scrambles the order of results. In this research pipeline, document order often reflects relevance (from Stage 2) or chronology (text chunks), so losing this order degrades the final synthesis quality.
**Action:** Always iterate over the list of futures in the order they were submitted (`for future in futures:`) instead of using `as_completed()` to maintain sequence while still benefiting from parallel execution.
