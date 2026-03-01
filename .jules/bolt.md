# BOLT'S JOURNAL - CRITICAL LEARNINGS ONLY

## 2025-05-15 - Parallelizing Stage 4 Scoring
**Learning:** Stage 4 (Academic Scoring) was previously sequential, creating a bottleneck as each document required a separate LLM call. By using `ThreadPoolExecutor`, we can process documents in parallel. Maintaining original document order is critical because earlier stages (Discovery) establish a relevance-based ranking that downstream stages (Filtering/Synthesis) may rely on.
**Action:** Use `ThreadPoolExecutor` and iterate over the list of futures in submission order to gather results, ensuring the ranked sequence of documents is preserved.
