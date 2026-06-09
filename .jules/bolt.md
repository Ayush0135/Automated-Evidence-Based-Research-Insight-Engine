## 2025-05-14 - Parallelization of Academic Scoring (Stage 4)
**Learning:** Parallelizing LLM API calls using `ThreadPoolExecutor` in Stage 4 significantly reduces total execution time. For 5 documents, execution time dropped from 5.00s to 2.00s using 3 workers. Order preservation was maintained by iterating over submitted futures in the original order.
**Action:** Use `ThreadPoolExecutor` for other I/O-bound stages (like Stage 3 analysis if not already fully optimized) and ensure a conservative `max_workers` (e.g., 3-5) to stay within API rate limits.
