from dataclasses import dataclass
from typing import List


@dataclass
class Intent:
    name: str
    confidence: float  # 0.0 – 1.0


@dataclass
class Gap:
    type: str          # cognitive | operational | decisional
    severity: float    # 0.0 – 1.0


@dataclass
class Brand:
    name: str
    domain: str
    allowed_intents: List[str]
    assets: List[str]


@dataclass
class DecisionContext:
    proximity_score: float  # 0.0 – 1.0


@dataclass
class UserInput:
    text: str
    context: DecisionContext
