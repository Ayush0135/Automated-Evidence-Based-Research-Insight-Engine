## 2025-05-15 - Order Scrambling via as_completed()
**Learning:** Using `concurrent.futures.as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 improved speed but introduced a quality bottleneck. It scrambled the relevance-based order of search results and the chronological sequence of document chunks, leading to lower quality synthesis in later stages.
**Action:** Always iterate over futures in their submission order when parallelizing I/O-bound tasks that depend on input sequence or ranking.
