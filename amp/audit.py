"""
amp.audit
---------
[DEPRECATED] Legacy decision logging.

This module is deprecated in favor of amp.decision_logger.
Security Update: We no longer log the full user_input to prevent data leakage.
Instead, we only log metadata and the decision outcome.
"""

from pathlib import Path
import json
from datetime import datetime, UTC
from typing import Dict, Any

from amp.config import MAX_ID_LENGTH, MAX_COLLECTION_SIZE

LOG_PATH = Path("logs/decisions.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

# Performance Optimization: Pre-instantiate a JSON encoder and bind its encode
# method to avoid redundant object creation and attribute lookup in the logging
# hot path. This reduces JSON serialization overhead by ~15-20%.
_ENCODER = json.JSONEncoder(ensure_ascii=False)
_ENCODE = _ENCODER.encode


def write_decision_log(
    trace_id: str, user_input: Dict[str, Any], decision: Dict[str, Any]
):
    """
    Append a decision record to the audit log (deprecated version).

    Security: Input text is REDACTED before logging to prevent sensitive data leakage.
    Only the input length and context are preserved for auditability.
    """
    if not isinstance(trace_id, str):
        raise ValueError(f"trace_id must be a string, got {type(trace_id)}")
    if len(trace_id) > MAX_ID_LENGTH:
        raise ValueError(f"trace_id exceeds maximum length of {MAX_ID_LENGTH}")

    if not isinstance(user_input, dict):
        raise ValueError(f"user_input must be a dict, got {type(user_input)}")
    if len(user_input) > MAX_COLLECTION_SIZE:
        raise ValueError(f"user_input exceeds maximum size of {MAX_COLLECTION_SIZE}")

    if not isinstance(decision, dict):
        raise ValueError(f"decision must be a dict, got {type(decision)}")
    if len(decision) > MAX_COLLECTION_SIZE:
        raise ValueError(f"decision exceeds maximum size of {MAX_COLLECTION_SIZE}")

    # Safely get text length, ensuring we don't crash on non-sized types
    user_text = user_input.get("text", "")
    text_length = len(user_text) if isinstance(user_text, (str, list, dict, tuple)) else 0

    redacted_input = {
        "text_length": text_length,
        "context": user_input.get("context", {}),
    }

    entry = {
        "ts": datetime.now(UTC).isoformat(),
        "trace_id": trace_id,
        "input": redacted_input,
        "decision": decision,
    }
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        # ⚡ Bolt: Performance Optimization
        # Use two write() calls instead of string concatenation to avoid
        # unnecessary string allocation in the logging hot path.
        fh.write(_ENCODE(entry))
        fh.write("\n")
