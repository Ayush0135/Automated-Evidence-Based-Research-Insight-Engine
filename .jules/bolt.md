## 2025-05-14 - ThreadPoolExecutor Order Preservation
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in this pipeline is a performance anti-pattern. While it returns results as they finish, it scrambles the document order, which is critical for maintaining the relevance-based ranking established in Stage 2 and the chronological sequence of text chunks in Stage 3.
**Action:** Always gather results by iterating over the list of futures in the order they were submitted to ensure input sequence is preserved.
