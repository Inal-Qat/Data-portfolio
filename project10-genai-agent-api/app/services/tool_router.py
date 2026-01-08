import re

_MATH_CHARS = re.compile(r"^[0-9\.\s\+\-\*\/\%\(\)\^]+$")

def looks_like_math(text: str) -> bool:
    t = text.strip()
    if len(t) < 3:
        return False
    # allow caret as pow alias
    t = t.replace("^", "**")
    return bool(_MATH_CHARS.match(t))
