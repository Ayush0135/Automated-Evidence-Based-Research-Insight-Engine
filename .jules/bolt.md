## 2025-05-14 - Parallelizing Stage 4 Academic Scoring
**Learning:** Document scoring (Stage 4) was previously sequential, making it a significant bottleneck as the number of research papers grew. Parallelizing it with `ThreadPoolExecutor` and 3 workers reduced mock execution time by 60% (from 5.00s to 2.00s for 5 docs).
**Action:** Use `ThreadPoolExecutor` for I/O-bound LLM scoring tasks, ensuring `max_workers` is tuned to balance speed against potential rate limits. Use a list of futures to maintain original document order during collection.
