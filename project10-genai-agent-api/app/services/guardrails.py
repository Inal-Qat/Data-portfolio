import re

INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"reveal (the )?system prompt",
    r"system prompt",
    r"you are now",
    r"act as",
]

def basic_guardrails(text: str) -> list[str]:
    warnings: list[str] = []
    lowered = text.lower()

    for pat in INJECTION_PATTERNS:
        if re.search(pat, lowered):
            warnings.append("possible_prompt_injection")
            break

    return warnings
