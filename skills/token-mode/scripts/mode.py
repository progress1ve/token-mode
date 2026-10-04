"""Persist a preference per chat without touching project or model settings."""
import argparse
import hashlib
import json
import os
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("mode", choices=["get", "economy", "detailed"])
p.add_argument("--chat", default=os.getenv("CODEX_THREAD_ID") or os.getenv("CODEX_SESSION_ID"))
p.add_argument("--state-dir", type=Path, default=Path.home() / ".agents/state/token-mode")
a = p.parse_args()
if not a.chat:
    p.error("Supply a stable --chat ID; never use a shared default ID.")
path = a.state_dir / (hashlib.sha256(a.chat.encode()).hexdigest()[:32] + ".json")
if a.mode != "get":
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps({"mode": a.mode}), encoding="utf-8")
    temp.replace(path)
mode = json.loads(path.read_text(encoding="utf-8"))["mode"] if path.exists() else "economy"
if mode not in ("economy", "detailed"):
    raise ValueError("Invalid state; explicitly select economy or detailed")
print("token-mode: " + mode)
