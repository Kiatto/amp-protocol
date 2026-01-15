from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="AMP Protocol Registry")

# Modello dati per il manifesto AMP
class AMPManifest(BaseModel):
    brand_name: str
    primary_domain: str
    intent_gates: List[str]
    value_hook: str
    action_endpoint: str

# Database simulato
registry = [
    {
        "brand_name": "Urban Context",
        "primary_domain": "sustainable_fashion",
        "intent_gates": ["viaggio minimalista", "abbigliamento tech", "capsule wardrobe"],
        "value_hook": "Guida al Minimalismo in Viaggio (5kg/7giorni)",
        "action_endpoint": "https://api.urbancontext.it/amp/subscribe"
    }
]

@app.get("/search")
async def match_intent(query: str):
    # Logica di matching semantico semplificata
    # TODO: Usare Supabase
    matches = [m for m in registry if any(gate in query.lower() for gate in m["intent_gates"])]
    return {"matches": matches}

@app.post("/handshake")
async def register_lead(email: str, brand_id: str):
    # Qui avviene la conversione reale
    return {"status": "success", "message": f"Iscrizione a {brand_id} completata per {email}"}