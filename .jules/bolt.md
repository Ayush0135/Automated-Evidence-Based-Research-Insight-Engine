## 2025-05-15 - Parallelization of Stage 4 Scoring
**Learning:** Serial LLM calls in the research pipeline (Stage 4) were a major bottleneck. Parallelizing with 3 workers achieved a 3x speedup while maintaining result order by iterating over futures in submission order.
**Action:** Always identify serial LLM call patterns in multi-stage pipelines and apply ThreadPoolExecutor with order preservation for network-bound tasks.

## 2025-05-15 - Token Efficiency in Stage 6 Synthesis
**Learning:** Large JSON objects in prompts (knowledge base) consume significant tokens and increase latency when indented. Removing indentation reduces the payload size without affecting LLM performance.
**Action:** Use json.dumps() without indentation for large data structures being injected into LLM prompts to minimize token costs and overhead.
