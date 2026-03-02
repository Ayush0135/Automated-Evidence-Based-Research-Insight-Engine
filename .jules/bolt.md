# Bolt Performance Journal

## 2025-05-15 - Order-Preserving Parallelism in Research Pipelines
**Learning:** In research pipelines where document relevance is established in early stages (e.g., Stage 2 Discovery), using `as_completed()` with `ThreadPoolExecutor` in downstream stages (Stage 3, 4) is a performance anti-pattern. While it executes tasks as they finish, it scrambles the document order, which degrades the quality of synthesis in later stages that expect relevance-ranked inputs.
**Action:** When parallelizing stages that process ordered lists of documents or text chunks, always iterate over the list of futures in submission order rather than using `as_completed()`. This ensures that even with parallel execution, the output sequence matches the input sequence.
