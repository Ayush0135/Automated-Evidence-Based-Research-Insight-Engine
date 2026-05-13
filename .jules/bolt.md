## 2025-05-15 - Parallelized Stage 4 Academic Scoring
**Learning:** Sequential LLM calls in research pipelines are a major I/O bottleneck. Parallelizing with ThreadPoolExecutor while iterating over submitted futures preserves document relevance/order.
**Action:** Always check for sequential LLM loops in processing stages and parallelize with order preservation where rankings matter.
