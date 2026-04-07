## 2025-05-14 - Missing Input Validation in Core Models and Logging
**Vulnerability:** The `Decision` dataclass and `write_decision_log` function lacked validation for string lengths, types, and numeric ranges.
**Learning:** Even internal protocols like AMP must enforce strict boundaries on data they process, especially when data originates from external callers (like `trace_id` in logging). Trusting inputs without validation can lead to log-based DoS or inconsistent state.
**Prevention:** Enforce string length limits (`MAX_TEXT_LENGTH`, `MAX_ID_LENGTH`) and type checks in `__post_init__` for all core models and at the entry points of utility functions.
