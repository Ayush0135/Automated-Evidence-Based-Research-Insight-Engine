## 2026-06-13 - Parallelized Stage 4 Scoring
**Learning:** Stage 4 (Academic Scoring) was a major bottleneck due to sequential LLM API calls. Parallelizing with a ThreadPoolExecutor (3 workers) reduced mock execution time from 5.00s to 2.00s for 5 documents, achieving a 2.5x speedup.
**Action:** Always consider parallelization for stages involving multiple independent I/O-bound LLM calls, but keep worker counts conservative (e.g., 3-5) to avoid hitting provider rate limits. Order preservation was not required here as downstream Stage 5 performs sorting.
