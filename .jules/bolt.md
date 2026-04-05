## 2025-05-22 - Sequential Future Iteration vs as_completed
**Learning:** In pipelines where the order of items (like document chunks or relevance-ranked search results) is critical for downstream quality, using `as_completed()` with `ThreadPoolExecutor` is a performance anti-pattern. While it processes results as soon as they are ready, it scrambles the logical chronology.
**Action:** Always iterate over the list of futures in the order they were submitted when parallelizing stages that require sequence preservation (Stages 2, 3, 4).
