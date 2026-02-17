import re

_MATH_CHARS = re.compile(r"^[0-9\.\s\+\-\*\/\%\(\)\^]+$")

def looks_like_math(text: str) -> bool:
    t = text.strip()
    if len(t) < 3:
        return False
    # allow caret as pow alias
    t = t.replace("^", "**")
    return bool(_MATH_CHARS.match(t))

def extract_timezone(text: str) -> str | None:
    t = text.lower()
    if "berlin" in t:
        return "Europe/Berlin"
    if "utc" in t or "gmt" in t:
        return "UTC"
    if "new york" in t or "nyc" in t:
        return "America/New_York"
    return None

def looks_like_time_query(text: str) -> bool:
    t = text.lower()
    return ("time" in t and ("in " in t or "utc" in t or "berlin" in t or "new york" in t)) or ("what time" in t)
