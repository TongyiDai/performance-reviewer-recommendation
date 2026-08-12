#!/usr/bin/env bash
set -euo pipefail

if ! command -v lark-cli >/dev/null 2>&1; then
  echo "blocked: lark-cli is not installed or not on PATH" >&2
  exit 1
fi

lark-cli --help >/dev/null

auth_out="$(lark-cli auth status --json --verify 2>&1 || true)"
if printf '%s' "$auth_out" | python3 -c 'import json,sys; p=json.load(sys.stdin); raise SystemExit(0 if p.get("identity") == "user" and p.get("verified") is True else 1)' 2>/dev/null; then
  echo "ok: verified user identity via auth status"
  exit 0
fi

if ! printf '%s' "$auth_out" | grep -Eqi 'unknown command|no such command|unrecognized command'; then
  echo "blocked: Lark authentication check failed; do not bypass a supported auth command" >&2
  exit 1
fi

contact_out="$(lark-cli contact +get-user --as user --json 2>/dev/null || true)"
if printf '%s' "$contact_out" | python3 -c 'import json,sys; p=json.load(sys.stdin); u=(p.get("data") or {}).get("user") or {}; raise SystemExit(0 if p.get("ok") is True and p.get("identity") == "user" and bool(u.get("open_id") or u.get("openId")) else 1)' 2>/dev/null; then
  echo "ok: resolved current user through read-only contact probe (auth status unavailable)"
  exit 0
fi

task_out="$(lark-cli task +get-my-tasks --as user --json 2>/dev/null || true)"
if printf '%s' "$task_out" | python3 -c 'import json,sys; p=json.load(sys.stdin); raise SystemExit(0 if p.get("ok") is True and p.get("identity") == "user" else 1)' 2>/dev/null; then
  echo "ok: user-context read canary passed; target tenant remains unbound"
  exit 0
fi

echo "blocked: no read-only user identity probe succeeded" >&2
exit 1
