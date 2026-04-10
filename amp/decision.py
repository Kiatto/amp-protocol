"""
amp.decision
------------
Builds the AMP Decision Record and defines the Decision dataclass.

Design decisions:
- `explanation` is a required keyword argument (no default).
  Omitting it raises TypeError, which enforces the protocol rule:
  every decision MUST be explainable. This is tested in test_decision_record.py.

- The build_decision_record function returns a plain dict (not a dataclass) so that it can be
  serialized to JSON without extra steps and consumed by any external system.

- We include a timestamp so that decision records are self-contained
  for auditability without depending on external logging infrastructure.
"""

from datetime import datetime, timezone, UTC
from typing import Any, Dict

from amp.models import Decision


def build_decision_record(
    outcome: str,
    intent: Dict[str, Any],
    gap: Dict[str, Any],
    context: Dict[str, Any],
    explanation: Dict[str, Any],  # ← required: no default value on purpose
) -> Dict[str, Any]:
    """
    Build a structured AMP Decision Record.

    Parameters
    ----------
    outcome     : one of NEUTRAL | INSIGHT_ONLY | HANDSHAKE_ALLOWED
    intent      : {"name": str, "confidence": float}
    gap         : {"type": str, "severity": float}
    context     : {"proximity_score": float}
    explanation : structured gate breakdown — MANDATORY by protocol rule

    Returns
    -------
    A plain dict ready for serialization or external handling.
    """
    if outcome not in Decision.ALLOWED_OUTCOMES:
        raise ValueError(f"Invalid decision outcome: {outcome}")

    if not isinstance(intent, dict):
        raise ValueError(f"intent must be a dict, got {type(intent)}")
    if not isinstance(gap, dict):
        raise ValueError(f"gap must be a dict, got {type(gap)}")
    if not isinstance(context, dict):
        raise ValueError(f"context must be a dict, got {type(context)}")
    if not isinstance(explanation, dict):
        raise ValueError(f"explanation must be a dict, got {type(explanation)}")

    return {
        "ts": datetime.now(UTC).isoformat(),
        "outcome": outcome,
        "intent": intent,
        "gap": gap,
        "context": context,
        "explanation": explanation,
    }
