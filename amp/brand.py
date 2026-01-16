from typing import Optional
from amp.models import Brand, Intent

CERTIFIED_BRANDS = [
    Brand(
        name="Urban Context",
        domain="Minimalist apparel / travel efficiency",
        allowed_intents=["EFFICIENCY_GAP", "WARDROBE_BUILDING"],
        assets=["5kg_travel_guide.pdf"],
    )
]


def select_eligible_brand(intent: Intent) -> Optional[Brand]:
    for brand in CERTIFIED_BRANDS:
        if intent.name in brand.allowed_intents:
            return brand
    return None
