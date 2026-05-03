## 2025-05-14 - Session-less requests anti-pattern
**Learning:** Using `requests.get()` directly in a high-volume research pipeline creates significant overhead due to repeated TCP/TLS handshakes, especially when querying the same API (Google) or downloading multiple papers from the same domain.
**Action:** Always use a persistent `requests.Session()` at the module or class level for any utility that performs multiple network requests to enable connection pooling.
