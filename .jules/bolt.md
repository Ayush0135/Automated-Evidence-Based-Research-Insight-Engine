## 2025-05-15 - Stage 4 Parallelization
**Learning:** Sequential LLM API calls in Stage 4 (Academic Scoring) were a significant I/O bottleneck. Parallelizing with a ThreadPoolExecutor (3 workers) provided a 3x speedup in mock benchmarks.
**Action:** Use ThreadPoolExecutor for I/O-bound LLM stages, ensuring results are gathered by iterating over futures in submission order to preserve document relevance ranking.
