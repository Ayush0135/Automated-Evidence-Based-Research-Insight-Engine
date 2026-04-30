## 2026-04-30 - Parallelization of Stage 4 Scoring
**Learning:** Sequential LLM calls in research pipelines create significant latency bottlenecks that can be safely mitigated with ThreadPoolExecutor since they are I/O-bound. Iterating over futures in submission order (rather than using as_completed) is essential for stages where input order corresponds to relevance ranking.
**Action:** Always check for sequential LLM loops in discovery, analysis, and scoring stages and apply parallelization with order preservation.
