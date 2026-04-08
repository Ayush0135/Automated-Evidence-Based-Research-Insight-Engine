# Bolt Performance Journal

## 2025-05-15 - Unordered Parallelism Anti-pattern in LLM Pipelines
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` for LLM tasks like document scoring or text chunk analysis is a performance anti-pattern in this codebase. While it allows starting processing of finished tasks early, it scrambles the document relevance ranking and the chronological order of text chunks, which degrades the quality of subsequent synthesis stages.
**Action:** Always gather results by iterating over the list of futures in the order they were submitted to preserve input sequence.

## 2025-05-15 - Prompt Token Efficiency
**Learning:** Using `indent` in `json.dumps()` when converting large objects like a research knowledge base into prompt text consumes unnecessary tokens and processing time for both the request and response.
**Action:** Use `json.dumps(obj)` without indentation for objects destined for LLM prompts to maximize context window utilization and reduce latency.
