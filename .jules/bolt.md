## 2025-05-14 - Order Preservation in Parallel Pipelines
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` is a performance anti-pattern for this research pipeline. While it improves throughput, it scrambles document relevance in Stage 2, document ranking in Stages 3 & 4, and chronological text sequence during chunk analysis. This degrades the quality of the synthesized knowledge base and final paper.
**Action:** Always gather results by iterating over the list of futures in submission order when order/relevance matters, even if it slightly delays the first available result.
