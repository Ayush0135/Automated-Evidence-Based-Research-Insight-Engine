## 2026-05-19 - Parallelizing LLM Scoring Pipeline
**Learning:** Sequential LLM calls in research pipelines are a major I/O bottleneck. Parallelizing with ThreadPoolExecutor (3 workers) reduced Stage 4 execution time by 60% (from 5s to 2s for 10 docs). Iterating over submitted futures in order is critical for maintaining the original relevance-based document ranking.
**Action:** Always identify sequential LLM loops and parallelize with order preservation if ranking or chronological sequence matters.
