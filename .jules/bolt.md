## 2025-05-15 - [Sequential Bottleneck in Stage 4]
**Learning:** Stage 4 (Academic Scoring) performs sequential API calls to Groq for each document, which is a major bottleneck when processing multiple documents. While other stages use `ThreadPoolExecutor`, Stage 4 was left sequential.
**Action:** Implement `ThreadPoolExecutor` in Stage 4 to match the parallelized pattern used in Stages 2 and 3.
