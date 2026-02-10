# Bolt's Journal - Critical Learnings

## 2025-05-14 - Parallelizing LLM Scoring
**Learning:** Sequential LLM calls in pipeline stages (like academic scoring) are a major bottleneck. Parallelizing with a conservative number of workers (e.g., 4) provides a 2x-4x speedup with minimal risk of hitting rate limits on high-throughput providers like Groq.
**Action:** Always check if loops containing LLM calls can be parallelized using ThreadPoolExecutor, especially for independent tasks like document analysis or scoring.
