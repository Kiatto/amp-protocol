"""
amp.agent
---------
Main AMP decision flow.

Design decisions:
- amp_agent_flow() now returns a Decision dataclass instead of a plain string.
  Reason: the protocol requires every outcome to be structured and explainable.
  Returning "Neutral response" was convenient but violated the core principle.

- We always build and return a Decision object, regardless of the outcome.
  NEUTRAL and INSIGHT_ONLY are valid, successful protocol executions — not errors.
  The Decision.reason field carries the human-readable explanation.

- The scores dict inside Decision captures all three sub-scores so that
  external systems and auditors can reproduce the PES calculation.

- Brand is None for NEUTRAL / INSIGHT_ONLY outcomes.
  It is only populated for HANDSHAKE_ALLOWED, after all gates have passed.
"""

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
from amp.decision import Decision


def amp_agent_flow(user_input: UserInput) -> Decision:
    """
    Run the full AMP decision flow.

    Returns a Decision object with outcome, scores, and explanation.
    Never raises — all unhappy paths are valid protocol outcomes.
    """

    intent = detect_intent(user_input)
    i_score = intent_score(intent)

    # --- Gate 1: intent threshold ---
    if intent.confidence < INTENT_THRESHOLD:
        return Decision(
            decision="NEUTRAL",
            pes=0.0,
            scores={"intent": i_score, "gap": 0.0, "timing": 0.0},
            reason=f"Intent confidence {intent.confidence:.2f} below threshold {INTENT_THRESHOLD}",
        )

    gap = identify_gap(user_input)
    g_score = gap_score(gap)

    # --- Gate 2: gap must exist ---
    if gap.severity == 0:
        return Decision(
            decision="INSIGHT_ONLY",
            pes=0.0,
            scores={"intent": i_score, "gap": g_score, "timing": 0.0},
            reason="No actionable gap detected",
        )

    t_score = timing_score(user_input.context)
    pes = promotion_eligibility_score(i_score, g_score, t_score)

    # --- Gate 3: PES threshold ---
    if pes < PES_THRESHOLD:
        return Decision(
            decision="INSIGHT_ONLY",
            pes=pes,
            scores={"intent": i_score, "gap": g_score, "timing": t_score},
            reason=f"PES {pes:.2f} below threshold {PES_THRESHOLD}",
        )

    brand = select_eligible_brand(intent)

    # --- Gate 4: a certified brand must match the intent ---
    if not brand:
        return Decision(
            decision="NEUTRAL",
            pes=pes,
            scores={"intent": i_score, "gap": g_score, "timing": t_score},
            reason=f"No certified brand found for intent '{intent.name}'",
        )

    return Decision(
        decision="HANDSHAKE_ALLOWED",
        pes=pes,
        scores={"intent": i_score, "gap": g_score, "timing": t_score},
        reason="All gates passed",
        brand={"name": brand.name, "domain": brand.domain},
    )
