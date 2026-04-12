## 2026-04-12 - [Parallelize Stage 4 Academic Scoring]
**Learning:** Stage 4 (Academic Scoring) was a sequential bottleneck in the research pipeline, as it performed LLM calls for each document one by one. Parallelizing this stage with a controlled number of workers (3) significantly improves throughput without overwhelming API rate limits.
**Action:** Use ThreadPoolExecutor for API-bound stages (Scoring, Analysis, Discovery) and ensure results are collected in submission order to preserve document relevance ranking.
