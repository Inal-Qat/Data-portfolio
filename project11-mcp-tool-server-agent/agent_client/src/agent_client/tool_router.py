import re

TIME_HINTS = ("time", "zeit", "uhr", "now", "current time", "date", "datum")

def choose_tool(user_input: str) -> str | None:
    """
    Route math-like expressions to calculator tool.
    """

    
    cleaned = user_input.strip().lower()

    if any(h in cleaned for h in TIME_HINTS):
        return "time_now_in_timezone"

    # Detect if string contains at least one math operator
    if any(op in cleaned for op in ["+", "-", "*", "/", "%"]):
        # Ensure it only contains allowed characters
        if re.fullmatch(r"[\d\.\+\-\*\/\(\)\s%]+", cleaned):
            return "calculator_safe_eval"

    return None