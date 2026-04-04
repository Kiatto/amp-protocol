from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class Intent:
    name: str
    confidence: float  # 0.0 – 1.0

    def __post_init__(self):
        # Strict validation as per memory instructions
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")


@dataclass(slots=True)
class Gap:
    type: str          # cognitive | operational | decisional
    severity: float    # 0.0 – 1.0

    def __post_init__(self):
        # Strict validation as per memory instructions
        if not (0.0 <= self.severity <= 1.0):
            raise ValueError(f"Severity must be between 0.0 and 1.0, got {self.severity}")


@dataclass(slots=True)
class Brand:
    name: str
    domain: str
    allowed_intents: List[str]
    assets: List[str]


@dataclass(slots=True)
class DecisionContext:
    proximity_score: float  # 0.0 – 1.0

    def __post_init__(self):
        # Strict validation as per memory instructions
        if not (0.0 <= self.proximity_score <= 1.0):
            raise ValueError(f"Proximity score must be between 0.0 and 1.0, got {self.proximity_score}")


@dataclass(slots=True)
class UserInput:
    text: str
    context: DecisionContext


@dataclass
class Decision:
    decision: str
    pes: float
    scores: dict
    reason: str
    brand: dict = None
