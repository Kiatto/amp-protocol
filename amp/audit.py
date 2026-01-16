from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any

LOG_PATH = Path("logs/decisions.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def write_decision_log(trace_id: str, user_input: Dict[str, Any], decision: Dict[str, Any]):
    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "trace_id": trace_id,
        "input": user_input,
        "decision": decision,
    }
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
