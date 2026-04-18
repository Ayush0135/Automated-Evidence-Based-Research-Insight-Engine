
## 2026-04-18 - Ordering Anti-pattern in Parallel Pipelines
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in research pipelines is a performance anti-pattern. While it maximizes individual task throughput, it scrambles document relevance and text chunk chronology. This degrades synthesis quality, potentially triggering more Stage 8 (Review) loops, which slows down the total time-to-paper.
**Action:** Always gather parallel results by iterating over the list of futures in submission order when sequence integrity (relevance or chronology) is required.
