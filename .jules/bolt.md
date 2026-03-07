## 2025-05-15 - Order Scrambling in Pipeline Parallelization
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 causes document relevance and text chunk chronology to be scrambled, which degrades the quality of downstream synthesis and filtering.
**Action:** Always iterate over the list of futures in submission order when gathering results from `ThreadPoolExecutor` in this pipeline to preserve the critical input sequence.
