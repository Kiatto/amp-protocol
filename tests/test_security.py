import pytest
from amp.models import Intent, Gap, DecisionContext, Decision

def test_intent_validation():
    # Valid
    Intent(name="test", confidence=0.0)
    Intent(name="test", confidence=0.5)
    Intent(name="test", confidence=1.0)

    # Invalid
    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        Intent(name="test", confidence=-0.1)
    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        Intent(name="test", confidence=1.1)

def test_gap_validation():
    # Valid
    Gap(type="test", severity=0.0)
    Gap(type="test", severity=0.5)
    Gap(type="test", severity=1.0)

    # Invalid
    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        Gap(type="test", severity=-0.1)
    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        Gap(type="test", severity=1.1)

def test_decision_context_validation():
    # Valid
    DecisionContext(proximity_score=0.0)
    DecisionContext(proximity_score=0.5)
    DecisionContext(proximity_score=1.0)

    # Invalid
    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        DecisionContext(proximity_score=-0.1)
    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        DecisionContext(proximity_score=1.1)

def test_decision_validation():
    # Valid
    Decision(decision="NEUTRAL", pes=0.0, scores={}, reason="test")
    Decision(decision="NEUTRAL", pes=0.5, scores={}, reason="test")
    Decision(decision="NEUTRAL", pes=1.0, scores={}, reason="test")

    # Invalid
    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        Decision(decision="NEUTRAL", pes=-0.1, scores={}, reason="test")
    with pytest.raises(ValueError, match="between 0.0 and 1.0"):
        Decision(decision="NEUTRAL", pes=1.1, scores={}, reason="test")
