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


def detect_intent(user_input: UserInput) -> Intent:
    """
    STUB: keyword-based intent detection.
    Replace with an LLM adapter or NLP classifier in production.
    """
    text = user_input.text.lower()

    if "viaggio" in text or "zaino" in text:
        return Intent(name="EFFICIENCY_GAP", confidence=0.9)

    return Intent(name="UNKNOWN", confidence=0.4)


def identify_gap(user_input: UserInput) -> Gap:
    """
    STUB: keyword-based gap identification.
    Replace with an LLM adapter or NLP classifier in production.
    """
    text = user_input.text.lower()

    if "zaino" in text or "leggero" in text:
        return Gap(type="operational", severity=0.8)

    return Gap(type="none", severity=0.0)
