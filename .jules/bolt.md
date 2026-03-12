## 2025-05-15 - Order-Breaking Parallelism Anti-pattern
**Learning:** Using `concurrent.futures.as_completed()` with `ThreadPoolExecutor` in Stages 3 and 4 scrambles the chronological order of text chunks and the relevance-based ranking of documents. This leads to degraded synthesis quality because downstream stages expect a specific logical sequence.
**Action:** When parallelizing I/O-bound LLM stages that rely on input sequence, iterate over the list of futures in the order they were submitted instead of using `as_completed()`.
