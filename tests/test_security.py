import pytest
from amp.models import UserInput, Decision, DecisionContext
from amp.config import MAX_TEXT_LENGTH

def test_user_input_length_limit():
    context = DecisionContext(proximity_score=0.5)

    # Valid length
    UserInput(text="a" * MAX_TEXT_LENGTH, context=context)

    # Exceeds limit
    with pytest.raises(ValueError, match=f"Input text exceeds maximum length of {MAX_TEXT_LENGTH} characters"):
        UserInput(text="a" * (MAX_TEXT_LENGTH + 1), context=context)

def test_user_input_type_check():
    context = DecisionContext(proximity_score=0.5)

    # Non-string input
    with pytest.raises(ValueError, match="Input text must be a string"):
        UserInput(text=123, context=context)

    with pytest.raises(ValueError, match="Input text must be a string"):
        UserInput(text=None, context=context)

def test_decision_pes_validation():
    scores = {"intent": 0.5, "gap": 0.5, "timing": 0.5}

    # Valid PES
    Decision(decision="NEUTRAL", pes=0.0, scores=scores, reason="test")
    Decision(decision="NEUTRAL", pes=1.0, scores=scores, reason="test")
    Decision(decision="NEUTRAL", pes=0.5, scores=scores, reason="test")

    # Invalid PES
    with pytest.raises(ValueError, match="PES must be between 0.0 and 1.0"):
        Decision(decision="NEUTRAL", pes=-0.1, scores=scores, reason="test")

    with pytest.raises(ValueError, match="PES must be between 0.0 and 1.0"):
        Decision(decision="NEUTRAL", pes=1.1, scores=scores, reason="test")
