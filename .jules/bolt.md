## 2025-05-14 - Parallelization and Order Preservation
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` is a performance anti-pattern in pipelines where input order (e.g., relevance-based document ranking) or chronological sequence (e.g., text chunks) must be preserved. While it allows processing results as they arrive, it scrambles the output sequence, which can degrade the quality of downstream stages like synthesis and filtering.
**Action:** To maintain order during parallelization, iterate directly over the list of futures in the order they were submitted (e.g., `for future in futures: result = future.result()`) instead of using `as_completed()`.

## 2025-05-14 - Stage 4 Parallelization
**Learning:** Sequential LLM calls in pipeline stages (like Academic Scoring) are major bottlenecks. Parallelizing these with a conservative number of workers (e.g., 3) provides a significant speedup (up to 3x) without hitting rate limits as aggressively as higher worker counts.
**Action:** Identified and parallelized Stage 4 (Academic Scoring) which was previously sequential.
