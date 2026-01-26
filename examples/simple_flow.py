"""
Minimal end-to-end example of the Agent Marketing Protocol (AMP).

This example demonstrates:
- intent evaluation
- decision outcome
- decision record generation
- optional external logging

No brands. No promotion delivery.
"""

import uuid

from amp.core.decision import build_decision_record
from amp.logging.decision_logger import write_decision_log


def main():
    # ------------------------------------------------------------------
    # 1. Simulated user interaction (already abstracted)
    # ------------------------------------------------------------------
    # NOTE: AMP does NOT operate on raw user text.
    # This is the result of a prior intent analysis step.
    intent = {
        "name": "EFFICIENCY_GAP",
        "confidence": 0.91,
    }

    gap = {
        "type": "operational",
        "severity": 0.8,
    }

    context = {
        "proximity_score": 0.9,
    }

    # ------------------------------------------------------------------
    # 2. Simulated decision logic (normally inside AMP core)
    # ------------------------------------------------------------------
    INTENT_THRESHOLD = 0.85
    PES_THRESHOLD = 0.70

    pes = 0.73  # Promotional Eligibility Score (example)

    if intent["confidence"] < INTENT_THRESHOLD:
        outcome = "NEUTRAL"
        explanation = {
            "intent_gate": "failed",
            "gap_gate": "not_evaluated",
            "timing_gate": "not_evaluated",
            "pes": pes,
            "thresholds": {
                "intent": INTENT_THRESHOLD,
                "pes": PES_THRESHOLD,
            },
        }
    elif pes < PES_THRESHOLD:
        outcome = "INSIGHT_ONLY"
        explanation = {
            "intent_gate": "passed",
            "gap_gate": "passed",
            "timing_gate": "failed",
            "pes": pes,
            "thresholds": {
                "intent": INTENT_THRESHOLD,
                "pes": PES_THRESHOLD,
            },
        }
    else:
        outcome = "HANDSHAKE_ALLOWED"
        explanation = {
            "intent_gate": "passed",
            "gap_gate": "passed",
            "timing_gate": "passed",
            "pes": pes,
            "thresholds": {
                "intent": INTENT_THRESHOLD,
                "pes": PES_THRESHOLD,
            },
        }

    # ------------------------------------------------------------------
    # 3. Build the AMP Decision Record
    # ------------------------------------------------------------------
    decision_record = build_decision_record(
        outcome=outcome,
        intent=intent,
        gap=gap,
        context=context,
        explanation=explanation,
    )

    # ------------------------------------------------------------------
    # 4. External handling (logging is OPTIONAL and external)
    # ------------------------------------------------------------------
    trace_id = str(uuid.uuid4())
    write_decision_log(trace_id, decision_record)

    # ------------------------------------------------------------------
    # 5. Output (for demonstration purposes only)
    # ------------------------------------------------------------------
    print("Decision Outcome:", outcome)
    print("Decision Record:")
    for key, value in decision_record.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
