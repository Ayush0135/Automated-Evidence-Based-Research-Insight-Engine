## 2024-04-14 - ThreadPoolExecutor Order Preservation
**Learning:** Using `as_completed(futures)` with `ThreadPoolExecutor` returns results as they finish, which scrambles the order of inputs. In a research pipeline, this degrades document relevance (Stage 2) and destroys text chronology in chunked analysis (Stage 3).
**Action:** Always iterate over the list of futures in submission order (`for f in futures: result = f.result()`) when the sequence of items is semantically important.
