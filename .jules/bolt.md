## 2025-05-15 - Parallelized Academic Scoring
**Learning:** Parallelizing LLM calls in Stage 4 significantly reduces total execution time. For 5 documents with a 1s mock latency, execution time dropped from 5s to 2s using 3 workers.
**Action:** Use `ThreadPoolExecutor` for stages with independent LLM calls, but keep worker counts low (3-5) to avoid aggressive rate limiting from providers like Groq or Gemini.
