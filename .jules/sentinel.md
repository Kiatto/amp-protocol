## 2025-05-14 - Missing Input Validation in Core Models and Logging
**Vulnerability:** The `Decision` dataclass and `write_decision_log` function lacked validation for string lengths, types, and numeric ranges.
**Learning:** Even internal protocols like AMP must enforce strict boundaries on data they process, especially when data originates from external callers (like `trace_id` in logging). Trusting inputs without validation can lead to log-based DoS or inconsistent state.
**Prevention:** Enforce string length limits (`MAX_TEXT_LENGTH`, `MAX_ID_LENGTH`) and type checks in `__post_init__` for all core models and at the entry points of utility functions.

## 2025-05-15 - Comprehensive Input Hardening
**Vulnerability:** Scattered missing type and length validations in `Brand` and `Decision` models, and the logging utility.
**Learning:** Defense-in-depth requires that *every* field in a public-facing or core data structure be validated, not just the most obvious ones (like user text). Omissions in secondary fields (like brand domains or score names) can still be exploited for log-spoofing or memory-based DoS.
**Prevention:** Use a "validation-by-default" approach in `__post_init__` for all dataclass fields and strictly type-check all arguments at the entry points of utility functions.

## 2025-05-16 - Hardening Deprecated Logging Paths
**Vulnerability:** The deprecated `amp.audit` module lacked the strict input validation implemented in its successor, creating a weak point for resource exhaustion or type-based crashes if legacy paths were still reachable.
**Learning:** Security hardening must be applied across the entire codebase, including deprecated modules, until they are fully removed. Inconsistent validation across similar components can be exploited by targeting the weakest implementation.
**Prevention:** Ensure that security updates are applied to all functional versions of a component (legacy and current) or explicitly remove the vulnerable legacy code.

## 2025-05-17 - Resource Exhaustion and Data Integrity in Logging and Models
**Vulnerability:** `write_decision_log` in `amp/decision_logger.py` could crash on missing `ts` fields and lacked collection size limits. The `Decision` model in `amp/models.py` did not validate the contents of the `brand` dictionary.
**Learning:** Hardening internal structures against malformed data is critical even when data is expected to come from internal protocol flows. Missing keys or oversized values in "metadata" fields (like brand info or timestamps) can lead to service instability (crashes) or log-based DoS.
**Prevention:** Always use safe retrieval (e.g., `.get()`) with explicit validation for mandatory fields in logging layers. Enforce size and type constraints on all nested dictionary contents in core data models.

## 2025-05-18 - Nested Data DoS in Decision Records
**Vulnerability:**  only performed shallow validation of input dictionaries. Maliciously large strings or collections nested within , , , or  could bypass length limits, leading to memory exhaustion or disk-space DoS during logging.
**Learning:** Shallow validation is insufficient for recursive data structures. If a dictionary is eventually serialized and logged, every nested element must be bounded.
**Prevention:** Implement recursive validation for all nested collections that originate from external input or are destined for persistent storage.

## 2025-05-18 - Nested Data DoS in Decision Records
**Vulnerability:** `build_decision_record` only performed shallow validation of input dictionaries. Maliciously large strings or collections nested within `intent`, `gap`, `context`, or `explanation` could bypass length limits, leading to memory exhaustion or disk-space DoS during logging.
**Learning:** Shallow validation is insufficient for recursive data structures. If a dictionary is eventually serialized and logged, every nested element must be bounded.
**Prevention:** Implement recursive validation for all nested collections that originate from external input or are destined for persistent storage.

## 2025-05-19 - Stack Exhaustion via Deeply Nested Collections
**Vulnerability:** The recursive validation logic in `_validate_collection` lacked a depth limit, allowing maliciously crafted deeply nested dictionaries or lists to trigger a `RecursionError` (stack overflow), leading to a Denial of Service (DoS).
**Learning:** Recursion without a depth limit is a security risk even if individual collection sizes are bounded. Stack space is a finite resource that must be protected when processing potentially hostile nested data.
**Prevention:** Always enforce a `MAX_DEPTH` constant in recursive validation functions to fail fast before exhausting the call stack.
