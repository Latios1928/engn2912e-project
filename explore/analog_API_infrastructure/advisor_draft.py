from __future__ import annotations

import json
import os
import random
import time
from dataclasses import dataclass
from pathlib import Path

OPENROUTER_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = os.environ.get("ADVISOR_MODEL","") #exact model slug from openrouter.ai/models
LOG_PATH = Path(os.environ.get("ADVISOR_LOG", "advisor_log.jsonl"))

SYSTEM_PROMPT = "  You are assisting with transistor sizing for a CMOS circuit in the GF180MCU 3.3 V process. You are given the tunable parameters with their bounds (SI units: metres), a table of already-simualted points with their measured metrics, and a target spec of acceptable ranges per metric. Propose new parameter sets that are likely to meet the spec. Reason from the trends in the data. Do not repeat points that were already simulated. Spread candidates out when the data is saprse; refine near the best point when it is close. Respond only wiht JSON matching the given schema. "

@dataclass(frozen=True)
class Param:
    name: str
    lo: float
    hi: float
    step: float

    def fix(self, x:float) -> float:
        x = min(max(float(x), self.lo), self.hi)
        snapped = self.lo + round((x-self.lo) / self.step) * self.step
        return round(min(snapped,self.hi),15)


Spec = dict[str, tuple[float,float]]

def meets_spec(metrics: dict, spec: Spec) -> bool: 
    return all(m in metrics and lo <= metrics[m] <= hi for m, (lo, hi) in spec.items())

def _key(params: dict, space: list[Param]) -> tuple: 
    return tuple(params[p.name] for p in space)

def _schema(space: list[Param]) -> dict: 
    candidate = {
        "type": "object",
        "properties": {p.name: {"type": "number"} for p in space}, 
        "required": [p.name for p in space],
        "additionalProperties": False
    }

    return {
        "name": "candidates",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "rationale": {"type": "string"},
                "candidates": {"type": "array", "items": candidate}
            },
            "required": ["rationale", "candidates"],
            "additionalProperties": False
        },
    }

def _user_prompt(space: list[Param], history: list[dict], spec: Spec, n: int) -> str: 
    lines = ["Parameters (name: lo .. hi, step):"]
    lines += [f" {p.name}: {p.lo} .. {p.hi:.4g}, step {p.step:.3g}" for p in space]

    lines.append("\nSpec (metric: acceptable range):")
    lines += [f" {m}: {lo} .. {hi:.4g}" for m, (lo, hi) in spec.items()]

    metrics = list(spec)
    lines.append("\nSimulated points:")
    if not history:
        lines.append(" (none yet)")
    else: 
        lines.append(" " + ",".join([p.name for p in space] + metrics + ["meets_spec"]))
        for h in history: 
            row = [f"{h['params'][p.name]:.4g}" for p in space]
            row += [f"{h['metrics'][m]:.4g}" for m in metrics]
            row.append(str(meets_spec(h['metrics'], spec)))
            lines.append(" " + ",".join(row))

        lines.append(f"\nPropose exactly {n} new candidates.")
        return "\n".join(lines)

def _log(record: dict) -> None: 
    with open(LOG_PATH, "a") as f: 
        f.write(json.dumps(record) + "\n")

def _random(space: list[Param], n: int) -> list[dict]: 
    return [{p.name: p.fix(random.uniform(p.lo, p.hi)) for p in space} for _ in range(n)]

def _client():
    from openai import OpenAI

    return OpenAI(base_url=OPENROUTER_URL, api_key=os.environ.get("OPENROUTER_API_KEY"))

def suggest(
        space: list[Param],
        history: list[dict],
        spec: Spec,
        n: int = 4,
        model: str | None = None,
        sub: bool = False,
        retries: int = 2,
) -> list[dict]:
    """
    Suggest new parameter sets to try, given a space of parameters, a history of already-simulated points, and a target spec.

    Args:
        space: List of Param objects defining the tunable parameters and their bounds.
        history: List of dicts containing previously simulated points with their parameters and measured metrics.
        spec: Dict mapping metric names to acceptable ranges (tuples of (lo, hi)).
        n: Number of new candidates to propose.
        model: Optional model slug from openrouter.ai/models. If None, uses DEFAULT_MODEL.
        sub: If True, returns a subset of candidates that meet the spec.
        retries: Number of times to retry the request in case of failure.


    
                     