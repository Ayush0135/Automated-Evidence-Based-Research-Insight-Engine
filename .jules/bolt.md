## 2025-05-22 - Parallelizing I/O-Bound LLM Stages
**Learning:** Sequential LLM calls in research pipelines create significant bottlenecks. Parallelizing Stage 4 (Academic Scoring) with 3 workers reduced execution time from ~5s to ~2s for 5 documents while maintaining document order.
**Action:** Always identify sequential I/O-bound loops (API calls, web scraping) and parallelize them using ThreadPoolExecutor while ensuring order preservation if required.
