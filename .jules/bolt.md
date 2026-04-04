## 2025-05-15 - [O(1) Brand Lookup Index]
**Learning:** Linear search ($O(N)$) over a registry (like certified brands) is a common but preventable bottleneck. Pre-computing a static index ($O(1)$) at module load time significantly reduces latency for core decision paths as the registry grows.
**Action:** Always identify static or slow-changing collections used in lookups and replace them with hash maps (dictionaries) or sets to ensure constant-time performance.
