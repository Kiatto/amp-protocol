import pytest
import json
from pathlib import Path
from amp.models import UserInput, Decision, DecisionContext, Intent, Gap, Brand
from amp.config import MAX_TEXT_LENGTH, MAX_ID_LENGTH, MAX_COLLECTION_SIZE, MAX_DEPTH
from amp.audit import write_decision_log as deprecated_write_decision_log
from amp.decision_logger import write_decision_log


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

    # Non-DecisionContext context
    with pytest.raises(ValueError, match="context must be a DecisionContext"):
        UserInput(text="valid", context="not-a-context")  # type: ignore


def test_decision_pes_validation():
    scores = {"intent": 0.5, "gap": 0.5, "timing": 0.5}

    # Valid PES
    Decision(decision="NEUTRAL", pes=0.0, scores=scores, reason="test")
    Decision(decision="NEUTRAL", pes=1.0, scores=scores, reason="test")
    Decision(decision="NEUTRAL", pes=0.5, scores=scores, reason="test")

    # Invalid PES type
    with pytest.raises(ValueError, match="PES must be a number"):
        Decision(decision="NEUTRAL", pes="not-a-number", scores=scores, reason="test")  # type: ignore

    # Invalid PES range
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

    # Wrong confidence type
    with pytest.raises(ValueError, match="Confidence must be a number"):
        Intent(name="VALID", confidence="not-a-number")  # type: ignore


def test_gap_type_validation():
    # Valid
    Gap(type="cognitive", severity=0.5)

    # Too long
    with pytest.raises(ValueError, match="Gap type exceeds maximum length"):
        Gap(type="A" * (MAX_ID_LENGTH + 1), severity=0.5)

    # Wrong type
    with pytest.raises(ValueError, match="Gap type must be a string"):
        Gap(type=123, severity=0.5)  # type: ignore

    # Wrong severity type
    with pytest.raises(ValueError, match="Severity must be a number"):
        Gap(type="cognitive", severity="not-a-number")  # type: ignore


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

    # Domain validation
    with pytest.raises(ValueError, match="Brand domain must be a string"):
        Brand(name="Valid", domain=123, allowed_intents=["INTENT"], assets=[])  # type: ignore

    with pytest.raises(ValueError, match="Brand domain exceeds maximum length"):
        Brand(
            name="Valid",
            domain="a" * (MAX_TEXT_LENGTH + 1),
            allowed_intents=["INTENT"],
            assets=[],
        )

    # allowed_intents validation
    with pytest.raises(ValueError, match="allowed_intents must be a list"):
        Brand(name="Valid", domain="valid.com", allowed_intents="INTENT", assets=[])  # type: ignore

    with pytest.raises(ValueError, match="Intent name must be a string"):
        Brand(name="Valid", domain="valid.com", allowed_intents=[123], assets=[])  # type: ignore

    with pytest.raises(ValueError, match="Intent name in allowed_intents exceeds"):
        Brand(
            name="Valid",
            domain="valid.com",
            allowed_intents=["A" * (MAX_ID_LENGTH + 1)],
            assets=[],
        )

    # Asset length validation
    with pytest.raises(ValueError, match="Asset path exceeds maximum length"):
        Brand(
            name="Valid",
            domain="valid.com",
            allowed_intents=["INTENT"],
            assets=["a" * (MAX_TEXT_LENGTH + 1)],
        )


def test_decision_reason_validation():
    scores = {"intent": 0.5, "gap": 0.5, "timing": 0.5}

    # Valid reason
    Decision(decision="NEUTRAL", pes=0.5, scores=scores, reason="valid reason")

    # Reason too long
    with pytest.raises(ValueError, match="Decision reason exceeds maximum length"):
        Decision(
            decision="NEUTRAL",
            pes=0.5,
            scores=scores,
            reason="a" * (MAX_TEXT_LENGTH + 1),
        )

    # Reason not a string
    with pytest.raises(ValueError, match="Decision reason must be a string"):
        Decision(decision="NEUTRAL", pes=0.5, scores=scores, reason=123)  # type: ignore


def test_decision_scores_validation():
    # Invalid scores type
    with pytest.raises(ValueError, match="scores must be a dict"):
        Decision(
            decision="NEUTRAL",
            pes=0.5,
            scores="not-a-dict",  # type: ignore
            reason="test",
        )

    # Invalid score value
    with pytest.raises(ValueError, match="Score 'intent' must be between 0.0 and 1.0"):
        Decision(
            decision="NEUTRAL",
            pes=0.5,
            scores={"intent": 1.1, "gap": 0.5, "timing": 0.5},
            reason="test",
        )

    with pytest.raises(ValueError, match="Score 'gap' must be between 0.0 and 1.0"):
        Decision(
            decision="NEUTRAL",
            pes=0.5,
            scores={"intent": 0.5, "gap": -0.1, "timing": 0.5},
            reason="test",
        )

    # Invalid score type
    with pytest.raises(ValueError, match="Score 'intent' must be a number"):
        Decision(
            decision="NEUTRAL",
            pes=0.5,
            scores={"intent": "not-a-number", "gap": 0.5, "timing": 0.5},  # type: ignore
            reason="test",
        )

    # Score name validation
    with pytest.raises(ValueError, match="Score name must be a string"):
        Decision(
            decision="NEUTRAL", pes=0.5, scores={123: 0.5}, reason="test"  # type: ignore
        )

    with pytest.raises(ValueError, match="Score name '.*' exceeds maximum length"):
        Decision(
            decision="NEUTRAL",
            pes=0.5,
            scores={"A" * (MAX_ID_LENGTH + 1): 0.5},
            reason="test",
        )


def test_write_decision_log_validation(tmp_path):
    log_file = tmp_path / "test_decisions_validation.jsonl"
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("amp.decision_logger.LOG_PATH", log_file)

        decision_record = {"ts": "2024-01-01", "outcome": "NEUTRAL"}

        # Valid trace_id
        write_decision_log("valid-trace", decision_record)

        # trace_id too long
        with pytest.raises(ValueError, match="trace_id exceeds maximum length"):
            write_decision_log("a" * (MAX_ID_LENGTH + 1), decision_record)

        # trace_id not a string
        with pytest.raises(ValueError, match="trace_id must be a string"):
            write_decision_log(123, decision_record)  # type: ignore

        # decision_record not a dict
        with pytest.raises(ValueError, match="decision_record must be a dict"):
            write_decision_log("trace", "not-a-dict")  # type: ignore

        # Missing 'ts' key
        with pytest.raises(ValueError, match="decision_record missing 'ts' field"):
            write_decision_log("trace-1", {"outcome": "NEUTRAL"})

        # Oversized record
        oversized_record = {f"k{i}": "v" for i in range(MAX_COLLECTION_SIZE + 1)}
        oversized_record["ts"] = "2024-01-01"
        with pytest.raises(ValueError, match="decision_record exceeds maximum size"):
            write_decision_log("trace-1", oversized_record)

        # Invalid ts type
        with pytest.raises(ValueError, match="timestamp 'ts' must be a string"):
            write_decision_log("trace-1", {"ts": 123, "outcome": "NEUTRAL"})

        # Oversized ts string (caught by deep validation first)
        with pytest.raises(ValueError, match="String at record.ts exceeds MAX_TEXT_LENGTH"):
            write_decision_log("trace-1", {"ts": "A" * (MAX_TEXT_LENGTH + 1), "outcome": "NEUTRAL"})

        # Deep validation in write_decision_log
        with pytest.raises(ValueError, match="Maximum nesting depth of .* exceeded at record.nested"):
            deep_record = {"ts": "2024-01-01"}
            curr = deep_record
            for _ in range(MAX_DEPTH + 1):
                curr["nested"] = {}
                curr = curr["nested"]
            write_decision_log("trace", deep_record)


def test_decision_context_validation():
    # Valid
    DecisionContext(proximity_score=0.5)

    # Invalid type
    with pytest.raises(ValueError, match="Proximity score must be a number"):
        DecisionContext(proximity_score="not-a-number")  # type: ignore

    # Invalid range
    with pytest.raises(ValueError, match="Proximity score must be between 0.0 and 1.0"):
        DecisionContext(proximity_score=1.1)


def test_decision_brand_validation():
    scores = {"intent": 0.5, "gap": 0.5, "timing": 0.5}

    # Valid
    Decision(
        decision="HANDSHAKE_ALLOWED",
        pes=0.5,
        scores=scores,
        reason="test",
        brand={"name": "test"},
    )

    # Invalid type
    with pytest.raises(ValueError, match="brand must be a dict or None"):
        Decision(
            decision="HANDSHAKE_ALLOWED",
            pes=0.5,
            scores=scores,
            reason="test",
            brand="not-a-dict",  # type: ignore
        )

    # Content validation for brand dict
    # Non-string value
    with pytest.raises(ValueError, match="Brand dictionary values must be strings"):
        Decision(
            decision="HANDSHAKE_ALLOWED",
            pes=0.5,
            scores=scores,
            reason="test",
            brand={"name": 123}  # type: ignore
        )

    # Oversized key
    with pytest.raises(ValueError, match="Brand dictionary key '.*' exceeds maximum length"):
        Decision(
            decision="HANDSHAKE_ALLOWED",
            pes=0.5,
            scores=scores,
            reason="test",
            brand={"A" * (MAX_ID_LENGTH + 1): "value"}
        )

    # Oversized value
    with pytest.raises(ValueError, match="Brand dictionary value for '.*' exceeds maximum length"):
        Decision(
            decision="HANDSHAKE_ALLOWED",
            pes=0.5,
            scores=scores,
            reason="test",
            brand={"name": "A" * (MAX_TEXT_LENGTH + 1)}
        )


def test_build_decision_record_validation():
    from amp.decision import build_decision_record

    valid_intent = {"name": "INTENT", "confidence": 0.9}
    valid_gap = {"type": "GAP", "severity": 0.8}
    valid_context = {"proximity_score": 0.7}
    valid_explanation = {"gate": "passed"}

    # Valid
    build_decision_record("NEUTRAL", valid_intent, valid_gap, valid_context, valid_explanation)

    # Invalid outcome
    with pytest.raises(ValueError, match="Invalid decision outcome"):
        build_decision_record("INVALID", valid_intent, valid_gap, valid_context, valid_explanation)

    # Invalid types
    with pytest.raises(ValueError, match="intent must be a dict"):
        build_decision_record("NEUTRAL", "not-a-dict", valid_gap, valid_context, valid_explanation)  # type: ignore

    with pytest.raises(ValueError, match="gap must be a dict"):
        build_decision_record("NEUTRAL", valid_intent, "not-a-dict", valid_context, valid_explanation)  # type: ignore

    with pytest.raises(ValueError, match="context must be a dict"):
        build_decision_record("NEUTRAL", valid_intent, valid_gap, "not-a-dict", valid_explanation)  # type: ignore

    with pytest.raises(ValueError, match="explanation must be a dict"):
        build_decision_record("NEUTRAL", valid_intent, valid_gap, valid_context, "not-a-dict")  # type: ignore


def test_build_decision_record_deep_validation():
    from amp.decision import build_decision_record

    valid_intent = {"name": "INTENT", "confidence": 0.9}
    valid_gap = {"type": "GAP", "severity": 0.8}
    valid_context = {"proximity_score": 0.7}
    valid_explanation = {"gate": "passed"}

    # Oversized nested string
    with pytest.raises(ValueError, match="String at intent.name exceeds MAX_TEXT_LENGTH"):
        build_decision_record("NEUTRAL", {"name": "A" * (MAX_TEXT_LENGTH + 1)}, valid_gap, valid_context, valid_explanation)

    # Oversized nested key
    with pytest.raises(ValueError, match="Dictionary key '.*' at intent exceeds MAX_ID_LENGTH"):
        build_decision_record("NEUTRAL", {"A" * (MAX_ID_LENGTH + 1): "val"}, valid_gap, valid_context, valid_explanation)

    # Nested collection limit
    with pytest.raises(ValueError, match="Collection at explanation.details exceeds MAX_COLLECTION_SIZE"):
        build_decision_record(
            "NEUTRAL",
            valid_intent,
            valid_gap,
            valid_context,
            {"details": [i for i in range(MAX_COLLECTION_SIZE + 1)]}
        )

    # Unsupported type in deep structure
    with pytest.raises(ValueError, match="Unsupported type .* at explanation.meta"):
        build_decision_record(
            "NEUTRAL",
            valid_intent,
            valid_gap,
            valid_context,
            {"meta": set([1, 2, 3])}
        )


def test_build_decision_record_recursion_limit():
    from amp.decision import build_decision_record

    valid_intent = {"name": "INTENT", "confidence": 0.9}
    valid_gap = {"type": "GAP", "severity": 0.8}
    valid_context = {"proximity_score": 0.7}

    # Deeply nested explanation
    deep_explanation = {}
    curr = deep_explanation
    for _ in range(MAX_DEPTH + 1):
        curr["a"] = {}
        curr = curr["a"]

    with pytest.raises(ValueError, match="Maximum nesting depth of .* exceeded at explanation"):
        build_decision_record("NEUTRAL", valid_intent, valid_gap, valid_context, deep_explanation)


def test_collection_size_limits():
    # Brand: allowed_intents limit
    with pytest.raises(ValueError, match="allowed_intents exceeds maximum size"):
        Brand(
            name="Test",
            domain="test.com",
            allowed_intents=["INTENT"] * (MAX_COLLECTION_SIZE + 1),
            assets=[],
        )

    # Brand: assets limit
    with pytest.raises(ValueError, match="assets exceeds maximum size"):
        Brand(
            name="Test",
            domain="test.com",
            allowed_intents=[],
            assets=["asset.pdf"] * (MAX_COLLECTION_SIZE + 1),
        )

    # Decision: scores limit
    with pytest.raises(ValueError, match="scores exceeds maximum size"):
        Decision(
            decision="NEUTRAL",
            pes=0.5,
            scores={f"score_{i}": 0.5 for i in range(MAX_COLLECTION_SIZE + 1)},
            reason="test",
        )

    # Decision: brand dict limit
    with pytest.raises(ValueError, match="brand exceeds maximum size"):
        Decision(
            decision="HANDSHAKE_ALLOWED",
            pes=0.5,
            scores={},
            reason="test",
            brand={f"key_{i}": "val" for i in range(MAX_COLLECTION_SIZE + 1)},
        )


def test_build_decision_record_collection_limits():
    from amp.decision import build_decision_record

    valid_item = {"a": 1}
    oversized_item = {f"k_{i}": i for i in range(MAX_COLLECTION_SIZE + 1)}

    # intent limit
    with pytest.raises(ValueError, match="Collection at intent exceeds MAX_COLLECTION_SIZE"):
        build_decision_record("NEUTRAL", oversized_item, valid_item, valid_item, valid_item)

    # gap limit
    with pytest.raises(ValueError, match="Collection at gap exceeds MAX_COLLECTION_SIZE"):
        build_decision_record("NEUTRAL", valid_item, oversized_item, valid_item, valid_item)

    # context limit
    with pytest.raises(ValueError, match="Collection at context exceeds MAX_COLLECTION_SIZE"):
        build_decision_record("NEUTRAL", valid_item, valid_item, oversized_item, valid_item)

    # explanation limit
    with pytest.raises(ValueError, match="Collection at explanation exceeds MAX_COLLECTION_SIZE"):
        build_decision_record("NEUTRAL", valid_item, valid_item, valid_item, oversized_item)


def test_audit_log_redaction(tmp_path):
    # Use a temporary log file for testing
    log_file = tmp_path / "test_decisions.jsonl"
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("amp.audit.LOG_PATH", log_file)

        trace_id = "test-trace"
        user_input = {"text": "SENSITIVE DATA", "context": {"user_id": 123}}
        decision = {"outcome": "NEUTRAL"}

        deprecated_write_decision_log(trace_id, user_input, decision)

        # Verify the log file content
        with open(log_file, "r") as f:
            entry = json.loads(f.read().strip())

        # Check redaction
        assert "text" not in entry["input"]
        assert entry["input"]["text_length"] == 14
        assert entry["input"]["context"]["user_id"] == 123
        assert entry["trace_id"] == trace_id


def test_deprecated_audit_log_validation(tmp_path):
    log_file = tmp_path / "test_deprecated_decisions_validation.jsonl"
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("amp.audit.LOG_PATH", log_file)

        valid_trace_id = "test-trace"
        valid_user_input = {"text": "test"}
        valid_decision = {"outcome": "NEUTRAL"}

        # Valid call
        deprecated_write_decision_log(valid_trace_id, valid_user_input, valid_decision)

        # trace_id validation
        with pytest.raises(ValueError, match="trace_id must be a string"):
            deprecated_write_decision_log(123, valid_user_input, valid_decision)  # type: ignore

        with pytest.raises(ValueError, match="trace_id exceeds maximum length"):
            deprecated_write_decision_log("A" * (MAX_ID_LENGTH + 1), valid_user_input, valid_decision)

        # user_input validation
        with pytest.raises(ValueError, match="user_input must be a dict"):
            deprecated_write_decision_log(valid_trace_id, "not-a-dict", valid_decision)  # type: ignore

        with pytest.raises(ValueError, match="user_input exceeds maximum size"):
            oversized_input = {f"k_{i}": i for i in range(MAX_COLLECTION_SIZE + 1)}
            deprecated_write_decision_log(valid_trace_id, oversized_input, valid_decision)

        # decision validation
        with pytest.raises(ValueError, match="decision must be a dict"):
            deprecated_write_decision_log(valid_trace_id, valid_user_input, "not-a-dict")  # type: ignore

        with pytest.raises(ValueError, match="decision exceeds maximum size"):
            oversized_decision = {f"k_{i}": i for i in range(MAX_COLLECTION_SIZE + 1)}
            deprecated_write_decision_log(valid_trace_id, valid_user_input, oversized_decision)
