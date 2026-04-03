import pytest
from amp.models import Intent, Gap, DecisionContext
from amp.scoring import (
    intent_score,
    gap_score,
    timing_score,
    promotion_eligibility_score,
)

def test_intent_score():
    intent = Intent(name="TESTK", confidence=0.85)
    assert intent_score(intent) == 0.85

def test_gap_score():
    gap = Gap(type="test", severity=0.6)
    assert gap_score(gap) == 0.6
    
    gap_zero = Gap(type="none", severity=-0.1)
    assert gap_score(gap_zero) == 0.0

def test_timing_score():
    ctx = DecisionContext(proximity_score=0.95)
    assert timing_score(ctx) == 0.95

def test_promotion_eligibility_score():
    assert promotion_eligibility_score(1.0, 1.0, 1.0) == 1.0
    assert promotion_eligibility_score(0.5, 0.5, 0.5) == 0.125
    assert promotion_eligibility_score(0.9, 0.8, 1.0) == pytest.approx(0.72)
