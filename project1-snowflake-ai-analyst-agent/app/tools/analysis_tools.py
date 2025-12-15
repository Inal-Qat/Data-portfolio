import re
from typing import Tuple, Optional


FORBIDDEN_KEYWORDS = {
    "drop", "delete", "update", "insert", "alter", "create", "truncate",
    "merge", "call", "grant", "revoke", "put", "get", "copy", "remove"
}

ALLOWED_START = ("select", "with")


def normalize_sql(sql: str) -> str:
    """Normalize whitespace and strip trailing semicolons/spaces."""
    s = sql.strip()
    # remove trailing semicolons
    s = re.sub(r";+\s*$", "", s)
    # normalize whitespace
    s = re.sub(r"\s+", " ", s)
    return s


def is_single_statement(sql: str) -> bool:
    """
    Reject multiple statements. A simple, practical heuristic:
    after stripping trailing semicolons, there should be no remaining ';'.
    """
    s = sql.strip()
    s = re.sub(r";+\s*$", "", s)
    return ";" not in s


def is_safe_sql(sql: str) -> Tuple[bool, Optional[str]]:
    """
    Allow only read-only SQL:
    - must start with SELECT or WITH
    - must not contain forbidden keywords
    - must be a single statement
    """
    s = normalize_sql(sql)
    lower = s.lower()

    if not is_single_statement(s):
        return False, "Rejected: multiple SQL statements are not allowed."

    if not lower.startswith(ALLOWED_START):
        return False, "Rejected: only SELECT/WITH queries are allowed."

    # Check forbidden keywords as whole words
    for kw in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", lower):
            return False, f"Rejected: forbidden keyword detected: {kw.upper()}"

    return True, None


def ensure_limit(sql: str, default_limit: int = 200) -> str:
    """
    If the query has no LIMIT clause, append LIMIT <default_limit>.
    Works for simple SELECT/WITH queries.
    """
    s = normalize_sql(sql)
    lower = s.lower()

    # If already has a LIMIT, keep it
    if re.search(r"\blimit\b\s+\d+", lower):
        return s

    # If it ends with a closing paren (rare), still okay to append
    return f"{s} LIMIT {default_limit}"

def compact_result_text(result_text: str, max_chars: int = 3000, head_lines: int = 25) -> str:
    """
    Reduce the size of a text table so it can be safely sent to the LLM.
    Keeps only the first N lines and truncates to max_chars.
    """
    if not result_text:
        return ""

    lines = result_text.splitlines()
    snippet = "\n".join(lines[:head_lines])

    if len(snippet) > max_chars:
        snippet = snippet[:max_chars] + "\n... (truncated)"

    # If original had more lines, mention it
    if len(lines) > head_lines:
        snippet += f"\n... ({len(lines) - head_lines} more lines omitted)"

    return snippet
