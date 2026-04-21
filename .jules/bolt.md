## 2026-04-21 - [Parallelizing Stage 4 Scoring]
**Learning:** Parallelizing I/O-bound LLM calls in pipeline stages significantly reduces total execution time. Using ThreadPoolExecutor and iterating over futures in submission order preserves document ranking and relevance, which is critical for downstream synthesis.
**Action:** Always prefer ordered future iteration over as_completed() when the sequence of items (like ranked search results) impacts the quality of the final output.
