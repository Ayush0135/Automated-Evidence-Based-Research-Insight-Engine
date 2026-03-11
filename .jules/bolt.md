## 2025-05-23 - Parallelizing Stage 4 Academic Scoring
**Learning:** Sequential LLM API calls in a pipeline are a major bottleneck. Parallelizing with `ThreadPoolExecutor` provides a linear speedup for I/O-bound tasks. However, using `as_completed()` is an anti-pattern when input order (relevance-based document ranking) must be preserved.
**Action:** Use `ThreadPoolExecutor` with a conservative worker count (e.g., 3-5) to avoid rate limits, and always iterate over the submitted futures list directly (in order) to maintain result sequence.
