import pytest
from unittest.mock import patch
from amp.models import UserInput, DecisionContext, Intent, Gap, Brand
from amp.agent import amp_agent_flow


@patch('amp.agent.detect_intent')
@patch('amp.agent.identify_gap')
@patch('amp.agent.select_eligible_brand')
def test_amp_agent_flow_success(mock_select_brand, mock_identify_gap, mock_detect_intent):
    mock_detect_intent.return_value = Intent(name="TEST_INTENT", confidence=0.9)
    mock_identify_gap.return_value = Gap(type="test", severity=0.9)
    mock_select_brand.return_value = Brand(
        name="Test Brand",
        domain="test",
        allowed_intents=["TEST_INTENT"],
        assets=[],
    )

    user_input = UserInput(
        text="test input",
        context=DecisionContext(proximity_score=1.0),  # PES = 0.9*0.9*1.0 = 0.81 >= 0.7
    )

    result = amp_agent_flow(user_input)

    # Decision is now a structured object, not a plain string
    assert result.decision == "HANDSHAKE_ALLOWED"
    assert result.brand["name"] == "Test Brand"
    assert result.pes > 0.7


@patch('amp.agent.detect_intent')
def test_amp_agent_flow_low_intent(mock_detect_intent):
    mock_detect_intent.return_value = Intent(name="WEAK", confidence=0.5)  # < 0.8

    user_input = UserInput(
        text="test input",
        context=DecisionContext(proximity_score=1.0),
    )

    result = amp_agent_flow(user_input)
    assert result.decision == "NEUTRAL"
    assert result.pes == 0.0
    assert "threshold" in result.reason


@patch('amp.agent.detect_intent')
@patch('amp.agent.identify_gap')
def test_amp_agent_flow_no_gap(mock_identify_gap, mock_detect_intent):
    mock_detect_intent.return_value = Intent(name="STRONG", confidence=0.9)
    mock_identify_gap.return_value = Gap(type="none", severity=0.0)

    user_input = UserInput(
        text="test input",
        context=DecisionContext(proximity_score=1.0),
    )

    result = amp_agent_flow(user_input)
    assert result.decision == "INSIGHT_ONLY"


@patch('amp.agent.detect_intent')
@patch('amp.agent.identify_gap')
def test_amp_agent_flow_low_pes(mock_identify_gap, mock_detect_intent):
    # PES = 0.9 * 0.5 * 1.0 = 0.45 < 0.7
    mock_detect_intent.return_value = Intent(name="STRONG", confidence=0.9)
    mock_identify_gap.return_value = Gap(type="partial", severity=0.5)

    user_input = UserInput(
        text="test input",
        context=DecisionContext(proximity_score=1.0),
    )

    result = amp_agent_flow(user_input)
    assert result.decision == "INSIGHT_ONLY"
    assert result.pes == pytest.approx(0.45)
