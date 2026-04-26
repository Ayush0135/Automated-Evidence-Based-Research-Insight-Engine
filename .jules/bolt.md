## 2025-05-14 - Parallelizing Stage 4 Academic Scoring
**Learning:** Sequential LLM API calls in Stage 4 were a major bottleneck, taking 5.0s for 10 documents. Parallelization with `ThreadPoolExecutor` and 3 workers reduced this to 2.0s (~2.5x speedup).
**Action:** Always check if multiple LLM calls can be parallelized, especially when order preservation is manageable by iterating over futures in submission order.

## 2025-05-14 - Importance of Order Preservation in Parallel Stages
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` scrambles results, which is a performance anti-pattern for this pipeline because it loses relevance-based ranking or chronological sequence.
**Action:** Use `for future in futures:` instead of `as_completed(futures)` when result order matters.
