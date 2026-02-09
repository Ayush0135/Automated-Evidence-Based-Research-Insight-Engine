## 2025-05-15 - Parallelize Stage 4 Scoring
**Learning:** Sequential LLM calls in pipeline stages (like Scoring) create significant bottlenecks, especially when processing multiple documents (up to 20). Parallelizing these calls with `ThreadPoolExecutor` drastically reduces execution time without significant complexity.
**Action:** Always check if a stage processes multiple independent items via LLM calls and parallelize them using a safe number of workers (e.g., 4-5) to balance speed and rate limits.
