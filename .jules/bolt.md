## 2025-05-15 - Sequential I/O Bottleneck in Research Stages
**Learning:** Research pipeline stages involving multiple LLM calls (like Stage 4 scoring) are significant I/O bottlenecks when executed sequentially. Parallelization with a moderate worker count (e.g., 3-5) provides substantial speedups without hitting rate limits prematurely.
**Action:** Always check for sequential LLM or network calls in processing loops and parallelize using `ThreadPoolExecutor` while ensuring result order is preserved by iterating over submitted futures.

## 2025-05-15 - Redundant Model Instantiation
**Learning:** Instantiating LLM model objects (like `genai.GenerativeModel`) inside a function that is called repeatedly introduces unnecessary overhead.
**Action:** Cache model instances at the module level or use a factory with memoization to reduce latency in hot paths.
