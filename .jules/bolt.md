## 2025-05-15 - Pipeline Parallelism and Order Preservation
**Learning:** In Stage 2, 3, and 4, using `as_completed()` with `ThreadPoolExecutor` is a performance anti-pattern because it scrambles document relevance and text chunk chronology, which degrades synthesis quality.
**Action:** Always iterate over the list of futures in submission order when using `ThreadPoolExecutor` to preserve input sequence, especially for relevance-ranked search results and chronological text chunks.

## 2025-05-15 - Stage 4 Parallelization
**Learning:** Stage 4 (Academic Scoring) was a major bottleneck as it processed documents sequentially with multiple LLM API calls.
**Action:** Parallelized Stage 4 using 3 workers, reducing execution time significantly while maintaining order.
