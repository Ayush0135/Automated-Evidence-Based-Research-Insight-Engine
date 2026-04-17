## 2026-04-17 - Parallelize Stage 4 Academic Scoring
**Learning:** Parallelizing Stage 4 Academic Scoring with 3 workers reduced mock execution time for 6 documents by 3x (from 3.00s to 1.00s). Using ThreadPoolExecutor is ideal for these I/O-bound LLM calls. Preserving order by iterating over futures in submission order ensures document ranking remains intact.
**Action:** Use parallelization for I/O-bound pipeline stages while being mindful of API rate limits and preserving input sequence order.
