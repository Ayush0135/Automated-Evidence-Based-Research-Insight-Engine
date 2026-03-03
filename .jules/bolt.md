## 2025-05-15 - Stage 4 Parallelization
**Learning:** Parallelizing Stage 4 (Academic Scoring) with 3 workers reduced execution time by 3x (from 6.00s to 2.00s for 6 documents) in a mock environment.
**Action:** Always maintain original document order when parallelizing by iterating over futures in submission order, as downstream stages may rely on document ranking.
