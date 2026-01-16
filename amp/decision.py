from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Decision:
    decision: str  # e.g. HANDSHAKE_ALLOWED, INSIGHT_ONLY, NEUTRAL
    pes: float
    scores: Dict[str, float]  # {"intent":.., "gap":.., "timing":..}
    reason: str
    brand: Optional[Dict[str, str]] = None  # {"name":..., "domain":...}
    trace_id: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "decision": self.decision,
            "pes": self.pes,
            "scores": self.scores,
            "reason": self.reason,
            "brand": self.brand,
            "trace_id": self.trace_id,
        }