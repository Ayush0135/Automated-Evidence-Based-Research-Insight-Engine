## 2025-05-15 - Order Preservation in Pipeline Stages
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 scrambles document relevance ranking and text chunk chronology, which can degrade the quality of synthesis and generation. Sequential iteration over submitted futures is required to maintain order.
**Action:** Always iterate over the list of futures in the order they were submitted when the sequence of items (like ranked search results or document chunks) impacts the final output quality.
