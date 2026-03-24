## 2025-05-15 - [Concurrency Order Anti-pattern]
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` is a performance anti-pattern in research pipelines where document relevance or text chronology matters. It introduces non-deterministic scrambling of results which degrades synthesis quality.
**Action:** Always gather results by iterating over the list of futures in submission order to preserve input sequence while maintaining parallel throughput.
