from amp.models import UserInput
from amp.intent import detect_intent, identify_gap
from amp.scoring import (
    intent_score,
    gap_score,
    timing_score,
    promotion_eligibility_score,
)
from amp.brand import select_eligible_brand
from amp.config import INTENT_THRESHOLD, PES_THRESHOLD


def amp_agent_flow(user_input: UserInput) -> str:
    intent = detect_intent(user_input)

    if intent.confidence < INTENT_THRESHOLD:
        return "Neutral response"

    gap = identify_gap(user_input)
    if gap.severity == 0:
        return "Insight-only response"

    pes = promotion_eligibility_score(
        intent_score(intent),
        gap_score(gap),
        timing_score(user_input.context),
    )

    if pes < PES_THRESHOLD:
        return "Insight-only response"

    brand = select_eligible_brand(intent)
    if not brand:
        return "Neutral response"

    return f"Handshake: ask consent to receive resource from {brand.name}"
