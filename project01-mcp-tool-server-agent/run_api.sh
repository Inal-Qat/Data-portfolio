#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"

export PYTHONPATH="$ROOT/agent_client/src:$ROOT/mcp_server/src:$ROOT/api/src"

# Run API
uvicorn api.main:app --host 0.0.0.0 --port 8000