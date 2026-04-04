## 2025-05-15 - Stage 4 Parallelization and Order Preservation
**Learning:** Sequential LLM calls in Stage 4 (Academic Scoring) were a major performance bottleneck for multi-document research. Using `as_completed` in Stages 2 and 3 was an order-preservation anti-pattern that could scramble relevance rankings and chunk chronology.
**Action:** Parallelized Stage 4 with 3 workers. Refactored Stages 2, 3, and 4 to gather results by iterating over futures in submission order instead of using `as_completed` to maintain deterministic output sequence while preserving throughput gains.
