## 2025-05-15 - Stage 4 Parallelization
**Learning:** Parallelizing Stage 4 with 3 workers reduced mock execution time for 6 documents by 3x (from 3.00s to 1.00s), achieving significant throughput gains while preserving document order.
**Action:** To maintain input sequence order when using ThreadPoolExecutor, iterate directly over the list of futures in the order they were submitted instead of using as_completed().
