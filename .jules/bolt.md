# Bolt's Performance Journal ⚡

## 2025-05-15 - Order-Preserving Parallelism in Stage 4
**Learning:** In this research pipeline, maintaining the relevance-based order of documents is critical for Stage 5 (Filtering) and Stage 6 (Synthesis). Using `as_completed()` with `ThreadPoolExecutor` scrambled the order, potentially degrading synthesis quality.
**Action:** When parallelizing pipeline stages that rely on input sequence (Stages 2, 3, 4), always iterate over the list of futures in submission order rather than using `as_completed()` to preserve ranking and chronological sequence.
