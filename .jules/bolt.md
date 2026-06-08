## 2025-05-14 - Parallelizing I/O-bound LLM Stages
**Learning:** Sequential LLM API calls in Stage 4 were a major bottleneck. Parallelizing with `ThreadPoolExecutor` and a small number of workers (3) provides a significant speedup (2.5x in benchmarks) without significantly increasing the risk of rate limiting.
**Action:** Always check for sequential network-bound operations and consider parallelization with a conservative worker count for LLM-heavy pipelines.

## 2025-05-14 - Dependency Mocking for Benchmarks
**Learning:** In restricted environments, benchmarks for modules with heavy external dependencies (like LLM clients) require comprehensive mocking of `sys.modules` to prevent `ModuleNotFoundError`.
**Action:** Use a `mock_modules` list and `sys.modules[m] = MagicMock()` pattern when bootstrapping test/benchmark scripts for pipeline stages.
