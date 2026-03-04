## 2025-05-15 - Parallelizing Stage 4 Academic Scoring
**Learning:** Parallelizing Stage 4 with 3 workers reduced mock execution time for 6 documents from 6.00s to 2.00s, achieving a 3x speedup. Iterating over futures in submission order is critical to preserve document relevance rankings established in earlier stages.
**Action:** When parallelizing I/O-bound pipeline stages, use ThreadPoolExecutor and iterate over the futures list in submission order to ensure results remain in the correct chronological or relevance sequence.
