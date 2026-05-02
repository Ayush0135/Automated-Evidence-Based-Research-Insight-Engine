## 2025-05-15 - Parallelization with Order Preservation
**Learning:** In pipelines where the sequence of data reflects priority (like relevance-ranked documents), using `concurrent.futures.as_completed()` is a performance anti-pattern because it scrambles the output order. Iterating over futures in the order they were submitted (`[f.result() for f in futures]`) preserves order while still providing the full speed benefit of parallel execution.
**Action:** Always prefer iterating over submitted futures in order when parallelizing stages that handle ranked or sequential data.
