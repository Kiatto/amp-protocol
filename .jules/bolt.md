## 2025-05-15 - [O(1) Brand Lookup Index]
**Learning:** Linear search ($O(N)$) over a registry (like certified brands) is a common but preventable bottleneck. Pre-computing a static index ($O(1)$) at module load time significantly reduces latency for core decision paths as the registry grows.
**Action:** Always identify static or slow-changing collections used in lookups and replace them with hash maps (dictionaries) or sets to ensure constant-time performance.

## 2025-05-16 - [Cached Derived State for Redundant Operations]
**Learning:** Redundant string operations (like `.lower()`) across multiple consumers of the same data object (like `UserInput`) can be eliminated by caching the derived state at initialization. This simplifies call sites and ensures the operation is performed exactly once per object lifecycle.
**Action:** When a data object is processed by multiple independent functions that all require the same transformation, move that transformation into the object's `__post_init__` (or similar) and cache the result.

## 2025-05-17 - [Inlining and Pre-Calculation for Hot Paths]
**Learning:** In Python, function call overhead and dictionary creation are measurable costs in performance-critical paths. Inlining simple property-access functions and pre-calculating static dictionaries (e.g., brand metadata) during object initialization can reduce decision flow latency by ~45%.
**Action:** Identify "hot" decision paths and replace frequent dictionary allocations with pre-calculated ones. Inline trivial scoring or lookup functions to avoid call stack overhead.

## 2025-05-20 - [Pre-instantiation of Static Data Objects]
**Learning:** Frequent instantiation and validation of dataclasses in hot paths (like Intent and Gap objects in the decision flow) can introduce measurable latency. Pre-instantiating common, static outcomes at the module level avoids redundant constructor calls and validation logic.
**Action:** For functions that frequently return the same set of static data objects, pre-instantiate them as module-level constants and reuse them.

## 2026-04-09 - [The Cost of Redundant Logic in Hot Paths]
**Learning:** Even simple built-in function calls like `max(x, 0.0)` contribute measurable overhead in Python's hot paths. If the range of a value is already guaranteed by strict dataclass validation, removing these redundant checks can reduce latency without sacrificing safety.
**Action:** Trust internal contract validations (like dataclass `__post_init__`) to avoid re-validating the same constraints in downstream execution logic.

## 2026-04-10 - [Pre-instantiating Complex Dataclasses for Common Exits]
**Learning:** For functions returning complex objects (like `Decision` with nested dictionaries and strict `__post_init__` validation), pre-instantiating common static outcomes at the module level can reduce path latency by over 90% (~15x speedup). Identity checks (`is`) provide an extremely fast branch to these cached results.
**Action:** Identify predictable or static exit points in hot paths and replace dynamic object instantiation with module-level constants.

## 2026-04-09 - [Micro-optimizations vs. Readability]
**Learning:** Extreme micro-optimizations like binding global constants to local variables or inlining high-level abstractions can yield measurable performance gains in Python but significantly degrade code readability and maintainability. These are often rejected during code review as "code smells."
**Action:** Balance performance gains with readability. Prioritize optimizations that simplify logic (like removing redundant calls) over those that obfuscate it for marginal nanosecond wins.
