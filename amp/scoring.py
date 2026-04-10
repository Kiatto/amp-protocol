from amp.models import Intent, Gap, DecisionContext


def intent_score(intent: Intent) -> float:
    return intent.confidence


def gap_score(gap: Gap) -> float:
    # Performance Optimization: Use gap.severity directly. Redundant max(..., 0.0)
    # removed as severity is already strictly validated to be within [0.0, 1.0]
    # in the Gap dataclass.
    return gap.severity


def timing_score(context: DecisionContext) -> float:
    return context.proximity_score


def promotion_eligibility_score(iscore: float, gscore: float, tscore: float) -> float:
    return iscore * gscore * tscore
