## 2025-05-14 - Parallelizing I/O-bound LLM stages
**Learning:** Sequential LLM calls are a major bottleneck in research pipelines. Parallelizing with `ThreadPoolExecutor` and preserving order via future submission order is a robust pattern. Mocking complex dependencies like `google-generativeai` and `dotenv` is necessary for isolated integration tests in restricted environments.
**Action:** Always look for sequential LLM or network calls and parallelize them using the `futures` list pattern to maintain result integrity.
