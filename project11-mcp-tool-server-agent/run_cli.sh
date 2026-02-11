#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$ROOT/agent_client/src:$ROOT/mcp_server/src"
python -m agent_client.cli "$@"
