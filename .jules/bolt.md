## 2025-05-15 - Parallelizing Stage 4 Academic Scoring
**Learning:** Sequential LLM API calls in Stage 4 created a significant bottleneck. Parallelizing with ThreadPoolExecutor (max_workers=3) provided a ~3x speedup for 6 documents while maintaining original document order by iterating over the futures list in submission order.
**Action:** Always check for sequential I/O-bound operations (like LLM calls or web searches) and parallelize them using ThreadPoolExecutor, ensuring order preservation where necessary for downstream logic.
