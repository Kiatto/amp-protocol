from amp.models import Intent, Gap, DecisionContext


def intent_score(intent: Intent) -> float:
    return intent.confidence


def gap_score(gap: Gap) -> float:
    return max(gap.severity, 0.0)


def timing_score(context: DecisionContext) -> float:
    return context.proximity_score


def promotion_eligibility_score(iscore: float, gscore: float, tscore: float) -> float:
    return iscore * gscore * tscore
