## 2025-05-15 - [Input validation for scores]
**Vulnerability:** Lack of input validation for security-critical scores (`confidence`, `severity`, `proximity_score`, `pes`) could allow logic bypasses or unexpected behavior if out-of-bounds values are provided.
**Learning:** AMP relies on several scores in the `[0.0, 1.0]` range to calculate the final Promotion Eligibility Score (PES). Without validation at the model level, an attacker or a buggy component could provide values like `10.0` to bypass intent gates or artificially inflate the PES.
**Prevention:** Use `__post_init__` in dataclasses to enforce range constraints on numeric scores at the moment of creation.
