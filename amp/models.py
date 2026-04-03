from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class Intent:
    name: str
    confidence: float  # 0.0 – 1.0

    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Intent confidence must be between 0.0 and 1.0, got {self.confidence}")


@dataclass
class Gap:
    type: str          # cognitive | operational | decisional
    severity: float    # 0.0 – 1.0

    def __post_init__(self):
        if not (0.0 <= self.severity <= 1.0):
            raise ValueError(f"Gap severity must be between 0.0 and 1.0, got {self.severity}")


@dataclass
class Brand:
    name: str
    domain: str
    allowed_intents: List[str]
    assets: List[str]


@dataclass
class DecisionContext:
    proximity_score: float  # 0.0 – 1.0

    def __post_init__(self):
        if not (0.0 <= self.proximity_score <= 1.0):
            raise ValueError(f"DecisionContext proximity_score must be between 0.0 and 1.0, got {self.proximity_score}")


@dataclass
class UserInput:
    text: str
    context: DecisionContext


@dataclass
class Decision:
    decision: str
    pes: float
    scores: Dict[str, float]
    reason: str
    brand: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not (0.0 <= self.pes <= 1.0):
            raise ValueError(f"Decision PES must be between 0.0 and 1.0, got {self.pes}")
