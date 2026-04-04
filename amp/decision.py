"""
amp.core.decision
-----------------
Builds the AMP Decision Record.

Design decisions:
- `explanation` is a required keyword argument (no default).
  Omitting it raises TypeError, which enforces the protocol rule:
  every decision MUST be explainable. This is tested in test_decision_record.py.

- The function returns a plain dict (not a dataclass) so that it can be
  serialized to JSON without extra steps and consumed by any external system.

- We include a timestamp so that decision records are self-contained
  for auditability without depending on external logging infrastructure.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class Decision:
    decision: str
    pes: float
    scores: Dict[str, float]
    reason: str
    brand: Optional[Dict[str, Any]] = field(default=None)

    def __post_init__(self):
        if not (0.0 <= self.pes <= 1.0):
            raise ValueError("pes must be between 0.0 and 1.0")


def build_decision_record(
    outcome: str,
    intent: Dict[str, Any],
    gap: Dict[str, Any],
    context: Dict[str, Any],
    explanation: Dict[str, Any],   # ← required: no default value on purpose
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

    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "outcome": outcome,
        "intent": intent,
        "gap": gap,
        "context": context,
        "explanation": explanation,
    }
