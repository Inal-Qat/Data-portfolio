import threading

_lock = threading.Lock()

_total_requests = 0
_total_success = 0
_total_errors = 0
_sum_latency_ms = 0
_last_latency_ms = 0


def record_request(success: bool, latency_ms: int) -> None:
    global _total_requests, _total_success, _total_errors, _sum_latency_ms, _last_latency_ms
    with _lock:
        _total_requests += 1
        _sum_latency_ms += int(latency_ms)
        _last_latency_ms = int(latency_ms)
        if success:
            _total_success += 1
        else:
            _total_errors += 1


def render_prometheus() -> str:
    with _lock:
        avg = (_sum_latency_ms / _total_requests) if _total_requests else 0.0

        lines = [
            "# HELP genai_api_requests_total Total number of /query requests",
            "# TYPE genai_api_requests_total counter",
            f"genai_api_requests_total {_total_requests}",
            "# HELP genai_api_requests_success_total Total number of successful /query requests",
            "# TYPE genai_api_requests_success_total counter",
            f"genai_api_requests_success_total {_total_success}",
            "# HELP genai_api_requests_error_total Total number of failed /query requests",
            "# TYPE genai_api_requests_error_total counter",
            f"genai_api_requests_error_total {_total_errors}",
            "# HELP genai_api_latency_ms_last Last observed request latency in ms",
            "# TYPE genai_api_latency_ms_last gauge",
            f"genai_api_latency_ms_last {_last_latency_ms}",
            "# HELP genai_api_latency_ms_avg Average request latency in ms",
            "# TYPE genai_api_latency_ms_avg gauge",
            f"genai_api_latency_ms_avg {avg}",
        ]
        return "\n".join(lines) + "\n"
