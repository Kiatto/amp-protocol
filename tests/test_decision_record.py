import pytest

from amp.core.decision import build_decision_record


def test_decision_record_requires_explanation():
    """
    AMP protocol rule:
    Every decision MUST include an explanation.
    """

    decision_record = build_decision_record(
        outcome="HANDSHAKE_ALLOWED",
        intent={"name": "EFFICIENCY_GAP", "confidence": 0.9},
        gap={"type": "operational", "severity": 0.8},
        context={"proximity_score": 0.9},
        explanation={
            "intent_gate": "passed",
            "gap_gate": "passed",
            "timing_gate": "passed",
            "pes": 0.72,
            "thresholds": {
                "intent": 0.85,
                "pes": 0.70,
            },
        },
    )

    assert "explanation" in decision_record, "Decision Record must include 'explanation'"
    assert isinstance(decision_record["explanation"], dict), "'explanation' must be a dict"
    assert decision_record["explanation"], "'explanation' must not be empty"


def test_decision_record_fails_without_explanation():
    """
    AMP fork-safety test:
    Removing explainability must break the protocol.
    """

    with pytest.raises(TypeError):
        # explanation is intentionally omitted
        build_decision_record(
            outcome="NEUTRAL",
            intent={"name": "UNKNOWN", "confidence": 0.2},
            gap={"type": "none", "severity": 0.0},
            context={"proximity_score": 0.1},
        )
