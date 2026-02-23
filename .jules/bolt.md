## 2025-05-14 - Parallelization Anti-pattern: as_completed()
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in this research pipeline is a performance anti-pattern. While it processes tasks as they finish, it scrambles document relevance ranking and text chunk chronology. This degradation in quality can lead to more iterations in the generation-review loop (Stage 7/8), ultimately slowing down the end-to-end process.
**Action:** Always iterate over futures in their submission order when gathering results for Stages 2, 3, and 4 to maintain deterministic and ranked output.
