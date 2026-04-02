## 2025-05-15 - [Order Preservation in Parallel Stages]
**Learning:** In this research pipeline, using `as_completed()` with `ThreadPoolExecutor` is a performance anti-pattern for Stages 2, 3, and 4. While it processes tasks as they finish, it scrambles document relevance ranking and text chunk chronology. Scrambled chunks in Stage 3 lead to incoherent summaries, and scrambled documents in Stage 2/4 degrade the quality of the final synthesis which expects relevance-ordered inputs.
**Action:** Always gather results by iterating over the list of futures in the order they were submitted (`for future in futures:`) to maintain sequence integrity while still gaining parallel throughput.

## 2025-05-15 - [Token Efficiency in Synthesis]
**Learning:** Using `indent=2` in `json.dumps()` when passing a large knowledge base to an LLM (Stage 6) consumes significant unnecessary tokens and increases processing latency without improving model performance.
**Action:** Use compact JSON (`json.dumps(obj)`) for large prompt contexts to maximize token efficiency and reduce cost/latency.
