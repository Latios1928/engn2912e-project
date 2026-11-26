#!/usr/bin/env python3
"""Compare finished runs (README milestone 8).

    python3 compare.py                       # every folder in runs/
    python3 compare.py runs/2026...random runs/2026...llm
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def best_curve(history: list[dict]) -> list[float]:
    """Best score after each simulation."""
    curve, best = [], float("inf")
    for h in history:
        if h.get("status") == "rejected":
            continue
        if h.get("score") is not None:
            best = min(best, h["score"])
        curve.append(best)
    return curve


def main(argv: list[str]) -> int:
    runs = [Path(a) for a in argv] or sorted(p for p in (HERE / "runs").glob("*") if p.is_dir())
    rows = []
    for r in runs:
        hist_path = r / "history.jsonl"
        if not hist_path.exists():
            continue
        hist = [json.loads(l) for l in hist_path.read_text().splitlines() if l.strip()]
        meta = json.loads((r / "meta.json").read_text()) if (r / "meta.json").exists() else {}
        curve = best_curve(hist)
        first = next((i + 1 for i, h in enumerate(h for h in hist if h.get("status") != "rejected")
                      if h.get("meets_spec")), None)
        rows.append((r.name, meta.get("model") or meta.get("proposer", "?"), len(curve),
                     sum(h.get("status") == "rejected" for h in hist), first,
                     curve[-1] if curve else float("nan")))
    print(f"{'run':32s} {'proposer/model':28s} {'sims':>5s} {'rej':>4s} {'1st pass':>8s} {'best':>8s}")
    for name, who, n, rej, first, best in rows:
        print(f"{name:32s} {str(who)[:28]:28s} {n:5d} {rej:4d} {str(first or '-'):>8s} {best:8.3g}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
