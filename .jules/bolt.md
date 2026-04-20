## 2025-05-15 - Order Preservation in Parallel Stages
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 is a performance anti-pattern. While it may seem slightly faster to process results as they arrive, it scrambles the relevance-based ranking of documents (Stages 2 & 4) and the chronological sequence of text chunks (Stage 3), leading to lower-quality research synthesis.
**Action:** Always gather results by iterating over the list of futures in their submission order: `for future in futures: result = future.result()`.
