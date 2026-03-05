## 2025-05-15 - [Stage 4 Parallelization]
**Learning:** Parallelizing Stage 4 with 3 workers reduced mock execution time for 6 documents from 6.00s to 2.00s, achieving a 3x speedup while preserving document order.
**Action:** Always gather results by iterating over futures in submission order to preserve relevance-based document ranking in sequential stages.
