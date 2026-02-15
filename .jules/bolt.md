## 2025-05-15 - Concurrency vs Order in Multi-Stage Pipelines

**Learning:** In pipelines where downstream stages depend on the relevance or chronological order of data (e.g., document ranking or text chunking), using `as_completed()` with `ThreadPoolExecutor` is a performance anti-pattern. While it processes individual results faster, it scrambles the order, leading to lower quality synthesis and potentially more rejected outputs in review stages, which increases the total pipeline execution time.

**Action:** For Stages 2, 3, and 4 in this codebase, always gather results by iterating over the list of futures in submission order to preserve relevance and chronology.
