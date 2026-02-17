from datetime import datetime
from zoneinfo import ZoneInfo

def now_in_timezone(tz: str) -> str:
    return datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")