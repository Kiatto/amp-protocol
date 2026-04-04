from dataclasses import dataclass
from typing import List


@dataclass
class Intent:
    name: str
    confidence: float  # 0.0 – 1.0

    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be between 0.0 and 1.0")


@dataclass
class Gap:
    type: str          # cognitive | operational | decisional
    severity: float    # 0.0 – 1.0

    def __post_init__(self):
        if not (0.0 <= self.severity <= 1.0):
            raise ValueError("severity must be between 0.0 and 1.0")


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
            raise ValueError("proximity_score must be between 0.0 and 1.0")


@dataclass
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
