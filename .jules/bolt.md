## 2025-05-15 - Stage 4 Parallelization
**Learning:** Parallelizing Stage 4 with 3 workers reduced mock execution time for 6 documents by 3x (from 3.00s to 1.00s), achieving significant throughput gains while preserving document order.
**Action:** When parallelizing, always iterate over the list of futures in submission order to preserve input sequence, especially for relevance-ranked lists.

## 2025-05-15 - Mocking Internal Modules for Benchmarking
**Learning:** When creating mock-based verification scripts, mock internal modules like `utils.llm` and `utils.search` by assigning them to `sys.modules` before importing any stages. This ensures that the stage logic uses the configured mocks instead of real API calls.
**Action:** Always set mock side effects or return values BEFORE the import statement in the benchmark script to ensure the target module receives the configured mock instance.
