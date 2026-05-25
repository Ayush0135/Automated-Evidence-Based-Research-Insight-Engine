## 2025-05-14 - Parallelization of Academic Scoring (Stage 4)
**Learning:** Sequential LLM calls in research pipelines are I/O bottlenecks and should be parallelized with order preservation (iterating over submitted futures) to maintain relevance rankings.
**Action:** Use ThreadPoolExecutor for I/O bound LLM tasks and ensure results are gathered via submission order to preserve ranking.
