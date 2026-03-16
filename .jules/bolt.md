## 2025-05-15 - Order scrambling anti-pattern in parallel stages
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 is a performance anti-pattern for this architecture. While it maximizes throughput, it scrambles document relevance rankings (Stage 2/4) and text chunk chronology (Stage 3), which degrades the quality of downstream synthesis and generation.
**Action:** Always gather results by iterating over the list of futures in submission order to preserve input sequence while maintaining parallelism.
