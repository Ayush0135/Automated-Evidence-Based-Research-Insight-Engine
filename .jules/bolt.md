## 2025-05-15 - [Stage 4 Parallelization]
**Learning:** Sequential LLM calls in research pipelines are a significant I/O bottleneck. Parallelizing with 3 workers reduced mock execution time from 5.00s to 2.00s for 5 documents while maintaining order.
**Action:** Always check for sequential API loops in stage-based pipelines and parallelize with order preservation (iterating over submitted futures).
