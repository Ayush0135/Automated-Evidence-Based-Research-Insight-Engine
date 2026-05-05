## 2026-05-05 - Connection Pooling in Search Utilities
**Learning:** Reusing TCP/TLS connections via `requests.Session()` significantly reduces latency in research pipelines that make multiple network requests to the same or different hosts.
**Action:** Always prefer `requests.Session()` for repeated I/O operations to minimize handshake overhead.
