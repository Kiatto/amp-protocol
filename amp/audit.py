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
from datetime import datetime, timezone
from typing import Dict, Any

LOG_PATH = Path("logs/decisions.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def write_decision_log(
    trace_id: str, user_input: Dict[str, Any], decision: Dict[str, Any]
):
    """
    Append a decision record to the audit log (deprecated version).

    Security: Input text is REDACTED before logging to prevent sensitive data leakage.
    Only the input length and context are preserved for auditability.
    """
    redacted_input = {
        "text_length": len(user_input.get("text", "")),
        "context": user_input.get("context", {}),
    }

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "trace_id": trace_id,
        "input": redacted_input,
        "decision": decision,
    }
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
