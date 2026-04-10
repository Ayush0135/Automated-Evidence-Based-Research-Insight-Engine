## 2025-01-24 - Document Order Preservation in Parallel Stages
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 is a performance anti-pattern because it scrambles the relevance-based order of documents and the chronological order of text chunks, which negatively impacts the quality of the final synthesis and paper generation.
**Action:** Always iterate over the list of futures in the order they were submitted to ensure that results are gathered in the correct sequence, even when processed in parallel.
