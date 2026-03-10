## 2024-03-10 - Ordering anti-pattern in ThreadPoolExecutor
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in this research pipeline is a performance anti-pattern. While it returns results as soon as they are ready, it scrambles the order of documents (relevance) and text chunks (chronology). This degradation of synthesis quality outweighs the minor latency benefit.
**Action:** When parallelizing Stage 2, 3, or 4, always gather results by iterating over the list of futures in submission order to preserve input sequence.
