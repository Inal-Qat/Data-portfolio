import re


def choose_tool(user_input: str) -> str | None:
    """
    Very simple rule-based routing:
    If input looks like math → use calculator tool.
    Otherwise → return None (LLM fallback).
    """

    math_pattern = r"^[\d\.\+\-\*\/\(\)\s%]+$"

    if re.match(math_pattern, user_input.strip()):
        return "calculator_safe_eval"

    return None