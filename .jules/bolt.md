## 2025-05-15 - [O(1) Brand Lookup Index]
**Learning:** Linear search ($O(N)$) over a registry (like certified brands) is a common but preventable bottleneck. Pre-computing a static index ($O(1)$) at module load time significantly reduces latency for core decision paths as the registry grows.
**Action:** Always identify static or slow-changing collections used in lookups and replace them with hash maps (dictionaries) or sets to ensure constant-time performance.

## 2025-05-16 - [Cached Derived State for Redundant Operations]
**Learning:** Redundant string operations (like `.lower()`) across multiple consumers of the same data object (like `UserInput`) can be eliminated by caching the derived state at initialization. This simplifies call sites and ensures the operation is performed exactly once per object lifecycle.
**Action:** When a data object is processed by multiple independent functions that all require the same transformation, move that transformation into the object's `__post_init__` (or similar) and cache the result.

## 2025-05-17 - [Inlining and Pre-Calculation for Hot Paths]
**Learning:** In Python, function call overhead and dictionary creation are measurable costs in performance-critical paths. Inlining simple property-access functions and pre-calculating static dictionaries (e.g., brand metadata) during object initialization can reduce decision flow latency by ~45%.
**Action:** Identify "hot" decision paths and replace frequent dictionary allocations with pre-calculated ones. Inline trivial scoring or lookup functions to avoid call stack overhead.
