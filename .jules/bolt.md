## 2025-05-14 - Stage 4 Parallelization
**Learning:** Parallelizing Stage 4 (Academic Scoring) with 3 workers reduced mock execution time for 6 documents by 3x (from 3.00s to 1.00s). Maintaining original document order is critical as downstream stages (Stage 5 Filtering) rely on the relevance established in earlier discovery.
**Action:** When parallelizing, always iterate over the list of futures in submission order rather than using `as_completed()` to preserve input sequence.
