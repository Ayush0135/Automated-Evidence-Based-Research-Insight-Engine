## 2025-05-14 - Parallelizing Stage 4 Scoring
**Learning:** Stage 4 (Academic Scoring) was previously sequential, causing a major bottleneck as each LLM call takes significant time. Downstream stages (Filtering, Synthesis) rely on the relevance-based document order established in earlier stages, so parallelization must preserve this order.
**Action:** Implement ThreadPoolExecutor with 3 workers in Stage 4 and gather results by iterating over futures in submission order to maintain ranking while gaining performance.
