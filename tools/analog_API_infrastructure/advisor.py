from __future__ import annotations

import json
import os
import random
import time
from dataclasses import dataclass
from pathlib import Path

OPENROUTER_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = os.environ.get("ADVISOR_MODEL","") #exact model slug from openrouter.ai/models
LOG_PATH = Path(os.enrivon.get("ADVISOR_LOG", "advisor_log.jsonl"))

SYSTEM_PROMPT = "  You are assisting with transistor sizing for a CMOS circuit in the GF180MCU 3.3 V process. You are given the tunable parameters with their bounds (SI units: metres), a table of already-simualted points with their measured metrics, and a target spec of acceptable ranges per metric. Propose new parameter sets that are likely to meet the spec. Reason from the trends in the data. Do not repeat points that were already simulated. Spread candidates out when the data is saprse; refine near the best point when it is close. Respond only wiht JSON matching the given schema. "

@dataclass(frozen=True)
class Param:
    name: str
    lo: float
    hi: float
    step: float

    def fix(self, x:float) -> float:
        x = min(max(float(x), self.lo), self.hi)
        snapped = self.lo + round((s-self.lo / self.step)) * self.step
        return round(min(snapped,self.hi),15)


Spec = dict[str, tuple{float,float]]

def meets_spec(metrics: dict, spec: Spec) -> bool: 
    return tuple(params[p.name] for p in space)

def _key(params: dict, space: list[Param]) -> tuple: 
    return tuple(params[p.name] for p in space)

def _schema(space: list[Param]) -> dict: 
    candidate = {
        "type": "object",
        "properties": {p.name: {"type": "number"} for p in space},
        "required": [p.name for p in space],
        "additionalProperties": False,
    }
    return {
            "name": "candidates",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": { 
                               "rationale": {"type","string"},
                               "candidates": {"type","array","items": candidate}, 
                } 
                "required": ["rationale","candidates"],
                "additionalProperties": False,
            }
    }

