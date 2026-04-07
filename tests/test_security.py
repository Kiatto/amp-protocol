import pytest
import json
from pathlib import Path
from amp.models import UserInput, Decision, DecisionContext, Intent, Gap, Brand
from amp.config import MAX_TEXT_LENGTH, MAX_ID_LENGTH
from amp.audit import write_decision_log


def test_user_input_length_limit():
    context = DecisionContext(proximity_score=0.5)

    # Valid length
    UserInput(text="a" * MAX_TEXT_LENGTH, context=context)

    # Exceeds limit
    with pytest.raises(
        ValueError,
        match=f"Input text exceeds maximum length of {MAX_TEXT_LENGTH} characters",
    ):
        UserInput(text="a" * (MAX_TEXT_LENGTH + 1), context=context)


def test_user_input_type_check():
    context = DecisionContext(proximity_score=0.5)

    # Non-string input
    with pytest.raises(ValueError, match="Input text must be a string"):
        UserInput(text=123, context=context)  # type: ignore

    with pytest.raises(ValueError, match="Input text must be a string"):
        UserInput(text=None, context=context)  # type: ignore


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


def test_decision_allowed_outcomes():
    scores = {"intent": 0.5, "gap": 0.5, "timing": 0.5}

    # Valid outcomes
    Decision(decision="NEUTRAL", pes=0.5, scores=scores, reason="test")
    Decision(decision="INSIGHT_ONLY", pes=0.5, scores=scores, reason="test")
    Decision(decision="HANDSHAKE_ALLOWED", pes=0.5, scores=scores, reason="test")

    # Invalid outcome
    with pytest.raises(ValueError, match="Invalid decision outcome: MALICIOUS_OUTCOME"):
        Decision(decision="MALICIOUS_OUTCOME", pes=0.5, scores=scores, reason="test")


def test_intent_name_validation():
    # Valid
    Intent(name="VALID_INTENT", confidence=0.5)

    # Too long
    with pytest.raises(ValueError, match="Intent name exceeds maximum length"):
        Intent(name="A" * (MAX_ID_LENGTH + 1), confidence=0.5)

    # Wrong type
    with pytest.raises(ValueError, match="Intent name must be a string"):
        Intent(name=123, confidence=0.5)  # type: ignore


def test_gap_type_validation():
    # Valid
    Gap(type="cognitive", severity=0.5)

    # Too long
    with pytest.raises(ValueError, match="Gap type exceeds maximum length"):
        Gap(type="A" * (MAX_ID_LENGTH + 1), severity=0.5)


def test_brand_security():
    # Valid
    Brand(
        name="Valid",
        domain="valid.com",
        allowed_intents=["INTENT"],
        assets=["guide.pdf"],
    )

    # Too long name
    with pytest.raises(ValueError, match="Brand name exceeds maximum length"):
        Brand(
            name="A" * (MAX_ID_LENGTH + 1),
            domain="valid.com",
            allowed_intents=["INTENT"],
            assets=["guide.pdf"],
        )

    # Path traversal and absolute paths in assets
    insecure_assets = [
        "../../etc/passwd",
        "/absolute/path",
        "C:\\Windows\\System32",
        "~/bashrc",
        "..\\local.settings.json",
    ]

    for asset in insecure_assets:
        with pytest.raises(
            ValueError, match="Insecure (asset|absolute) path detected"
        ):
            Brand(
                name="Valid",
                domain="valid.com",
                allowed_intents=["INTENT"],
                assets=[asset],
            )

    # Type check for assets
    with pytest.raises(ValueError, match="Asset path must be a string"):
        Brand(
            name="Valid",
            domain="valid.com",
            allowed_intents=["INTENT"],
            assets=[123],  # type: ignore
        )


def test_audit_log_redaction(tmp_path):
    # Use a temporary log file for testing
    log_file = tmp_path / "test_decisions.jsonl"
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("amp.audit.LOG_PATH", log_file)

        trace_id = "test-trace"
        user_input = {"text": "SENSITIVE DATA", "context": {"user_id": 123}}
        decision = {"outcome": "NEUTRAL"}

        write_decision_log(trace_id, user_input, decision)

        # Verify the log file content
        with open(log_file, "r") as f:
            entry = json.loads(f.read().strip())

        # Check redaction
        assert "text" not in entry["input"]
        assert entry["input"]["text_length"] == 14
        assert entry["input"]["context"]["user_id"] == 123
        assert entry["trace_id"] == trace_id
