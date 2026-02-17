import json
import sys
from datetime import datetime


def log_event(event: dict):
    """
    Emit structured JSON log line.
    """
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        **event
    }
    print(json.dumps(payload), file=sys.stderr)