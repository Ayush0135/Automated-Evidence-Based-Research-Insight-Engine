# Bolt's Journal - Critical Learnings

## 2025-02-22 - Parallelization Order Preservation
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 is a performance anti-pattern. While it might seem faster to process results as they arrive, it scrambles document relevance (Stage 2/4) and text chunk chronology (Stage 3). This degradation in input quality leads to poor synthesis and triggers expensive regeneration loops in the Review stage, increasing total execution time and cost.
**Action:** Always maintain input sequence order when parallelizing I/O-bound stages by iterating over the list of futures in submission order instead of using `as_completed()`.
