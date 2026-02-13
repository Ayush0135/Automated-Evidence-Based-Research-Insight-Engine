# Bolt's Journal - Research Agent Optimizations

## 2025-05-14 - Parallel Execution vs Sequence Integrity
**Learning:** In a multi-stage research pipeline, maintaining the relevance-based order of documents (from search results) and the chronological order of text chunks (during analysis) is critical for downstream quality. Using `as_completed()` with `ThreadPoolExecutor` provides non-deterministic results that scramble this order, potentially leading to lower quality synthesis or hallucinations in the final paper.
**Action:** Always prefer direct iteration over futures (e.g., `[f.result() for f in futures]`) instead of `as_completed()` when sequence order matters for the next stage. Use `max_workers=3` for LLM scoring stages to balance speed and rate-limit safety.
