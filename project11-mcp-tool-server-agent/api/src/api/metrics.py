from prometheus_client import Counter, Histogram

# --- Request-level metrics ---
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)

HTTP_REQUEST_LATENCY_MS = Histogram(
    "http_request_latency_ms",
    "HTTP request latency in milliseconds",
    ["path"],
    buckets=(5, 10, 25, 50, 100, 250, 500, 1000, 2000, 5000),
)

# --- Agent-level metrics ---
AGENT_RUNS_TOTAL = Counter(
    "agent_runs_total",
    "Total agent runs",
    ["route"],  # tool|llm
)

TOOL_CALLS_TOTAL = Counter(
    "tool_calls_total",
    "Total tool calls",
    ["tool_name"],
)

TOOL_LATENCY_MS = Histogram(
    "tool_latency_ms",
    "Tool call latency in milliseconds",
    ["tool_name"],
    buckets=(2, 5, 10, 25, 50, 100, 250, 500, 1000, 2000),
)

LLM_LATENCY_MS = Histogram(
    "llm_latency_ms",
    "LLM call latency in milliseconds",
    buckets=(50, 100, 200, 300, 500, 800, 1200, 2000, 5000, 10000),
)