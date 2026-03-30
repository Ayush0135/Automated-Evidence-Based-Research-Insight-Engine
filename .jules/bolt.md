## 2025-05-14 - ThreadPoolExecutor Order Preservation
**Learning:** Using `as_completed(futures)` with `ThreadPoolExecutor` returns results in completion order, which can scramble data that depends on input sequence (like document relevance ranking).
**Action:** To preserve input sequence, iterate directly over the list of futures in the order they were submitted: `for future in futures: result = future.result()`.
