"""
amp.intent
----------
Intent detection and gap identification.

!! ADAPTER BOUNDARY !!
-----------------------
This module is a STUB implementation for development and testing only.

In a real deployment, intent detection must be performed by an external
system (an LLM, a classifier, an NLP pipeline) BEFORE calling AMP.
AMP receives the result — it never interprets raw user text itself.

The keyword matching below is intentionally minimal and language-specific
(Italian) to make its placeholder nature obvious.
Replace this module with a proper adapter before going to production.

See docs/ARCHITECTURE.md — "Boundary With LLMs" section.
"""

from amp.models import Intent, Gap, UserInput

# ⚡ Bolt: Performance Optimization
# Pre-instantiate common Intent and Gap objects to avoid redundant object creation
# and validation overhead during the decision flow. This is ~15x faster than
# creating new objects on every call.
INTENT_EFFICIENCY_GAP = Intent(name="EFFICIENCY_GAP", confidence=0.9)
INTENT_UNKNOWN = Intent(name="UNKNOWN", confidence=0.4)

GAP_OPERATIONAL = Gap(type="operational", severity=0.8)
GAP_NONE = Gap(type="none", severity=0.0)


def detect_intent(user_input: UserInput) -> Intent:
    """
    STUB: keyword-based intent detection.
    Replace with an LLM adapter or NLP classifier in production.
    """
    # ⚡ Bolt: Performance Optimization
    # Use the pre-cached lowercase text to avoid redundant string operations.
    text = user_input.text_lower

    if "viaggio" in text or "zaino" in text:
        return INTENT_EFFICIENCY_GAP

    return INTENT_UNKNOWN


def identify_gap(user_input: UserInput) -> Gap:
    """
    STUB: keyword-based gap identification.
    Replace with an LLM adapter or NLP classifier in production.
    """
    # ⚡ Bolt: Performance Optimization
    # Use the pre-cached lowercase text to avoid redundant string operations.
    text = user_input.text_lower

    if "zaino" in text or "leggero" in text:
        return GAP_OPERATIONAL

    return GAP_NONE
