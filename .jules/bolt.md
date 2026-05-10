## 2025-05-14 - Parallelizing I/O-bound LLM Scoring
**Learning:** Sequential LLM calls in research pipelines are major I/O bottlenecks. Using ThreadPoolExecutor with order-preserving iteration over futures provides significant throughput gains without disrupting ranking logic.
**Action:** Always identify sequential loops containing network requests (API calls) and parallelize them using ThreadPoolExecutor, ensuring results are gathered in original order if ranking matters.
