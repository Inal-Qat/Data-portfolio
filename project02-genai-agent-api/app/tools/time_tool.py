from datetime import datetime
from zoneinfo import ZoneInfo

def now_in_timezone(tz_name: str) -> str:
    """
    Return current time in ISO format for a given IANA timezone.
    Examples: "Europe/Berlin", "UTC", "America/New_York"
    """
    tz = ZoneInfo(tz_name)
    return datetime.now(tz).isoformat(timespec="seconds")
