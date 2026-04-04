from typing import Optional, Dict
from amp.models import Brand, Intent

# List of brands certified by the protocol.
# In a real-world scenario, this might be loaded from an external registry or database.
CERTIFIED_BRANDS = [
    Brand(
        name="Urban Context",
        domain="Minimalist apparel / travel efficiency",
        allowed_intents=["EFFICIENCY_GAP", "WARDROBE_BUILDING"],
        assets=["5kg_travel_guide.pdf"],
    )
]

# ⚡ Bolt: Performance Optimization
# Pre-computed index mapping each intent name to its primary eligible brand.
# This replaces a linear O(N_brands * N_intents) search with an O(1) dictionary lookup,
# which is critical for low-latency decision flows as the registry of certified brands grows.
BRAND_INTENT_INDEX: Dict[str, Brand] = {}
for brand in CERTIFIED_BRANDS:
    for intent_name in brand.allowed_intents:
        if intent_name not in BRAND_INTENT_INDEX:
            BRAND_INTENT_INDEX[intent_name] = brand


def select_eligible_brand(intent: Intent) -> Optional[Brand]:
    """
    Selects a certified brand that is eligible for the given intent.

    Uses a pre-computed O(1) index for optimal performance.
    """
    return BRAND_INTENT_INDEX.get(intent.name)
