## 2026-04-19 - Pipeline Parallelization and Order Preservation
**Learning:** Using as_completed() with ThreadPoolExecutor is a performance anti-pattern in research pipelines because it scrambles document relevance and chunk chronology, potentially leading to quality-based rejections and retries. Parallelizing Stage 4 scoring significantly reduces end-to-end latency.
**Action:** Always iterate over futures in submission order when sequence matters for synthesis quality.
