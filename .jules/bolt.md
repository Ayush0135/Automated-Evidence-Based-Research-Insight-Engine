## 2025-05-24 - Avoiding as_completed for Pipeline Integrity
**Learning:** In a multi-stage research pipeline, `as_completed()` with `ThreadPoolExecutor` is a performance anti-pattern. While it returns results as they finish, it scrambles document relevance (Stage 2/4) and text chronology (Stage 3 chunks), which severely degrades the quality of the final synthesis.
**Action:** Always iterate over the list of futures in the order they were submitted to maintain sequence integrity across stages.
