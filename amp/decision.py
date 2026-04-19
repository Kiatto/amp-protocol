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

import math
from datetime import datetime, timezone, UTC
from typing import Any, Dict, List, Union

from amp.config import MAX_COLLECTION_SIZE, MAX_TEXT_LENGTH, MAX_ID_LENGTH, MAX_DEPTH
from amp.models import Decision


def _validate_collection(data: Any, path: str = "", depth: int = 0) -> None:
    """
    Recursively validate that a collection (dict or list) only contains
    allowed types and adheres to size/length limits.
    """
    # ⚡ Bolt: Performance Optimization
    # Recursion depth check to prevent stack exhaustion and resource-based DoS.
    if depth > MAX_DEPTH:
        raise ValueError(
            f"Maximum nesting depth of {MAX_DEPTH} exceeded at {path or 'root'}"
        )

    if isinstance(data, dict):
        if len(data) > MAX_COLLECTION_SIZE:
            raise ValueError(
                f"Collection at {path or 'root'} exceeds MAX_COLLECTION_SIZE"
            )
        for k, v in data.items():
            if not isinstance(k, str):
                raise ValueError(
                    f"Dictionary key at {path} must be a string, got {type(k)}"
                )
            if len(k) > MAX_ID_LENGTH:
                raise ValueError(f"Dictionary key '{k}' at {path} exceeds MAX_ID_LENGTH")

            # ⚡ Bolt: Performance Optimization
            # Unrolled recursion for leaf nodes and lazy path construction.
            # Scalar types and strings are validated inline to avoid redundant calls.
            if isinstance(v, (int, float, bool)):
                if not math.isfinite(v):
                    new_path = f"{path}.{k}" if path else k
                    raise ValueError(f"Non-finite numeric value at {new_path}")
                continue

            if v is None:
                continue

            if isinstance(v, str):
                if len(v) > MAX_TEXT_LENGTH:
                    new_path = f"{path}.{k}" if path else k
                    raise ValueError(f"String at {new_path} exceeds MAX_TEXT_LENGTH")
                continue

            new_path = f"{path}.{k}" if path else k
            _validate_collection(v, new_path, depth + 1)

    elif isinstance(data, list):
        if len(data) > MAX_COLLECTION_SIZE:
            raise ValueError(
                f"Collection at {path or 'root'} exceeds MAX_COLLECTION_SIZE"
            )
        for i, item in enumerate(data):
            # ⚡ Bolt: Performance Optimization
            # Leaf node unrolling for lists.
            if isinstance(item, (int, float, bool)):
                if not math.isfinite(item):
                    new_path = f"{path}[{i}]"
                    raise ValueError(f"Non-finite numeric value at {new_path}")
                continue

            if item is None:
                continue

            if isinstance(item, str):
                if len(item) > MAX_TEXT_LENGTH:
                    new_path = f"{path}[{i}]"
                    raise ValueError(f"String at {new_path} exceeds MAX_TEXT_LENGTH")
                continue

            new_path = f"{path}[{i}]"
            _validate_collection(item, new_path, depth + 1)

    elif isinstance(data, str):
        if len(data) > MAX_TEXT_LENGTH:
            raise ValueError(f"String at {path or 'root'} exceeds MAX_TEXT_LENGTH")

    elif isinstance(data, (int, float, bool)):
        if not math.isfinite(data):
            raise ValueError(f"Non-finite numeric value at {path or 'root'}")

    elif data is None:
        pass
    else:
        raise ValueError(f"Unsupported type {type(data)} at {path or 'root'}")


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
    _validate_collection(intent, "intent")

    if not isinstance(gap, dict):
        raise ValueError(f"gap must be a dict, got {type(gap)}")
    _validate_collection(gap, "gap")

    if not isinstance(context, dict):
        raise ValueError(f"context must be a dict, got {type(context)}")
    _validate_collection(context, "context")

    if not isinstance(explanation, dict):
        raise ValueError(f"explanation must be a dict, got {type(explanation)}")
    _validate_collection(explanation, "explanation")

    return {
        "ts": datetime.now(UTC).isoformat(),
        "outcome": outcome,
        "intent": intent,
        "gap": gap,
        "context": context,
        "explanation": explanation,
    }
