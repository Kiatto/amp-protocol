from amp.models import Intent, Gap, UserInput


def detect_intent(user_input: UserInput) -> Intent:
    text = user_input.text.lower()

    if "viaggio" in text or "zaino" in text:
        return Intent(name="EFFICIENCY_GAP", confidence=0.9)

    return Intent(name="UNKNOWN", confidence=0.4)


def identify_gap(user_input: UserInput) -> Gap:
    text = user_input.text.lower()

    if "zaino" in text or "leggero" in text:
        return Gap(type="operational", severity=0.8)

    return Gap(type="none", severity=0.0)
