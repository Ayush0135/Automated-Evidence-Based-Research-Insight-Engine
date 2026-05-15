## 2026-05-15 - [Parallelized Stage 4 Scoring]
**Learning:** Sequential LLM calls in research pipelines are major I/O bottlenecks. Using ThreadPoolExecutor for independent document processing significantly reduces latency without compromising document order.
**Action:** Always look for loops containing 'query_stage' or specific LLM callers (query_groq, query_gemini) as prime candidates for parallelization using ThreadPoolExecutor.
