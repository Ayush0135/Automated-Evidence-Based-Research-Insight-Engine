## 2025-05-15 - Order Preservation Anti-pattern in ThreadPoolExecutor
**Learning:** Using `as_completed(futures)` with `ThreadPoolExecutor` scrambled document relevance in Stage 2 and chunk chronology in Stage 3, leading to lower-quality synthesis even if execution was parallel.
**Action:** Always iterate over the list of futures in the order they were submitted (`for f in futures: f.result()`) when the input sequence must be preserved.

## 2025-05-15 - Stage 4 Scoring Bottleneck
**Learning:** Stage 4 was performing sequential LLM calls for academic scoring, creating a significant bottleneck (3.0s for 6 docs). Parallelizing with 3 workers reduced this to 1.0s (3x speedup).
**Action:** Use a `score_single_document` helper and `ThreadPoolExecutor` for high-volume LLM scoring tasks.
