## 2025-05-22 - [Maintaining Order in Parallelized LLM Pipelines]
**Learning:** In multi-stage research pipelines, the order of documents often reflects their relevance (e.g., from initial search results). Parallelizing I/O-bound tasks like LLM scoring with `as_completed` can shuffle this order, potentially degrading the quality of downstream synthesis if they assume relevance-based ranking.
**Action:** Always iterate over a list of futures in submission order instead of using `as_completed` when the sequence of documents or chunks matters for subsequent stages.
