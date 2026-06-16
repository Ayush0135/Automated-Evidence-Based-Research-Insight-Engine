## 2025-05-14 - Parallelization of I/O Bound LLM Calls in Stage 4
**Learning:** Stage 4 (Academic Scoring) was a major sequential bottleneck in the research pipeline because it made one synchronous LLM call per document. Parallelizing with `ThreadPoolExecutor` and 3 workers resulted in a 2.5x speedup for 5 documents in benchmarks.
**Action:** Always check for sequential loops containing LLM calls or network I/O and consider parallelizing them with a conservative worker count to avoid rate limits.
