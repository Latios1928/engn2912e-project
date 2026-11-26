"""OpenRouter advisor: asks a language model for new candidate parameter sets.

Same structure as advisor_draft.py (the user's draft), completed:
- Param, Spec, meets_spec, _key, _schema, _user_prompt, _log, _random: as in the draft, bugs fixed
- _post: the HTTP call (standard library only, no `openai` package needed)
- _parse: JSON from the reply, with a fallback for models without structured output
- suggest: one round (prompt -> API -> parse -> clamp/snap -> drop duplicates)

The model only proposes. Every value is clamped and snapped with Param.fix,
duplicates of simulated points are dropped, and loop.py validates again
before anything is simulated.

Environment:
    OPENROUTER_API_KEY  required for suggest()
    ADVISOR_MODEL       default model slug from openrouter.ai/models
    ADVISOR_LOG         where prompts/replies are logged (loop.py sets this per run)
"""
from __future__ import annotations

import json
import math
import os
import random
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = os.environ.get("ADVISOR_MODEL", "")
LOG_PATH = Path(os.environ.get("ADVISOR_LOG", "advisor_log.jsonl"))
TIMEOUT_S = 120

# History sent to the model is trimmed to the best K plus the most recent M points.
KEEP_BEST = 20
KEEP_RECENT = 20

SYSTEM_PROMPT = (
    "You are assisting with transistor and bias sizing for an analog CMOS circuit "
    "in the GF180MCU 3.3 V process. You are given the tunable parameters with their "
    "bounds and grid steps (SI units: metres, volts), a target spec of acceptable "
    "ranges per metric, and a table of already-simulated points with their measured "
    "metrics (nan = the measurement failed, e.g. the circuit did not spike). "
    "Propose new parameter sets that are likely to meet the spec. Reason from the "
    "trends in the data. Do not repeat points that were already simulated. Spread "
    "candidates out when the data is sparse; refine near the best point when it is "
    "close. Respond only with JSON matching the given schema."
)


@dataclass(frozen=True)
class Param:
    name: str
    lo: float
    hi: float
    step: float

    def fix(self, x: float) -> float:
        x = min(max(float(x), self.lo), self.hi)
        snapped = self.lo + round((x - self.lo) / self.step) * self.step
        return float(f"{min(snapped, self.hi):.12g}")


Spec = dict[str, tuple[float, float]]


def _ok(x) -> bool:
    return isinstance(x, (int, float)) and not math.isnan(x)


def meets_spec(metrics: dict, spec: Spec) -> bool:
    return all(_ok(metrics.get(m)) and lo <= metrics[m] <= hi for m, (lo, hi) in spec.items())


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
                "rationale": {"type": "string"},
                "candidates": {"type": "array", "items": candidate},
            },
            "required": ["rationale", "candidates"],
            "additionalProperties": False,
        },
    }


def _bound(x: float) -> str:
    return "none" if math.isinf(x) else f"{x:.4g}"


def _distance(metrics: dict, spec: Spec) -> float:
    """Rough distance from spec, used only to pick which history rows to keep."""
    d = 0.0
    for m, (lo, hi) in spec.items():
        x = metrics.get(m)
        if not _ok(x):
            d += 10.0
        elif x < lo:
            d += (lo - x) / max(abs(lo), 1e-30)
        elif x > hi:
            d += (x - hi) / max(abs(hi), 1e-30)
    return d


def _trim(history: list[dict], spec: Spec) -> list[dict]:
    if len(history) <= KEEP_BEST + KEEP_RECENT:
        return history
    best = sorted(range(len(history)), key=lambda i: _distance(history[i]["metrics"], spec))[:KEEP_BEST]
    keep = set(best) | set(range(len(history) - KEEP_RECENT, len(history)))
    return [history[i] for i in sorted(keep)]


def _user_prompt(space: list[Param], history: list[dict], spec: Spec, n: int) -> str:
    lines = ["Parameters (name: lo .. hi, step):"]
    lines += [f"  {p.name}: {p.lo:.4g} .. {p.hi:.4g}, step {p.step:.4g}" for p in space]

    lines.append("\nSpec (metric: acceptable range, 'none' = unbounded):")
    lines += [f"  {m}: {_bound(lo)} .. {_bound(hi)}" for m, (lo, hi) in spec.items()]

    metrics = list(spec)
    shown = _trim(history, spec)
    lines.append("\nSimulated points:" if len(shown) == len(history) else
                 f"\nSimulated points ({len(shown)} of {len(history)}: best and most recent):")
    if not shown:
        lines.append("  (none yet)")
    else:
        lines.append("  " + ",".join([p.name for p in space] + metrics + ["meets_spec"]))
        for h in shown:
            row = [f"{h['params'][p.name]:.4g}" for p in space]
            row += [f"{h['metrics'].get(m, float('nan')):.4g}" for m in metrics]
            row.append(str(meets_spec(h["metrics"], spec)))
            lines.append("  " + ",".join(row))

    lines.append(f"\nPropose exactly {n} new candidates.")
    return "\n".join(lines)


def _log(record: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")


def _random(space: list[Param], n: int) -> list[dict]:
    return [{p.name: p.fix(random.uniform(p.lo, p.hi)) for p in space} for _ in range(n)]


class AdvisorError(RuntimeError):
    pass


def _post(body: dict) -> dict:
    """POST to OpenRouter; returns the decoded JSON response.
    Raises urllib.error.HTTPError on HTTP errors (caller decides on retries)."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise AdvisorError("OPENROUTER_API_KEY is not set")
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
        return json.loads(r.read().decode())


def _parse(text: str) -> dict:
    """JSON object from the reply. Tolerates ```json fences or text around it."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise AdvisorError("no JSON object in reply")
    return json.loads(m.group(0))


def suggest(
    space: list[Param],
    history: list[dict],
    spec: Spec,
    n: int = 4,
    model: str | None = None,
    retries: int = 2,
) -> list[dict]:
    """
    Ask the model for up to n new parameter sets.

    Args:
        space: tunable parameters (anything with name/lo/hi/step/fix).
        history: simulated points, each {"params": {...}, "metrics": {...}};
            a failed measurement is nan or missing.
        spec: {metric: (lo, hi)}; use -inf/inf for an open bound.
        n: number of candidates to ask for.
        model: OpenRouter model slug; defaults to $ADVISOR_MODEL.
        retries: extra attempts after an HTTP 429/5xx, a network error or an
            unparsable reply (with exponential backoff).

    Returns:
        Candidates clamped and snapped to the grid, with duplicates of the
        history (and of each other) removed, so possibly fewer than n.
        An empty list means the model gave nothing usable.
    """
    model = model or DEFAULT_MODEL
    if not model:
        raise AdvisorError("no model: pass model= or set ADVISOR_MODEL")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _user_prompt(space, history, spec, n)},
    ]
    structured = True   # switched off if the model rejects response_format
    raw = None

    for attempt in range(retries + 1):
        body = {"model": model, "messages": messages, "temperature": 0.7}
        if structured:
            body["response_format"] = {"type": "json_schema", "json_schema": _schema(space)}
        else:   # no schema enforcement: describe the format in the prompt instead
            example = {"rationale": "...", "candidates": [{p.name: p.lo for p in space}]}
            body["messages"] = messages + [{"role": "user", "content":
                "Reply with only a JSON object of this form, no other text:\n" + json.dumps(example)}]
        rec = {"t": time.time(), "model": model, "attempt": attempt,
               "structured": structured, "messages": messages}
        t0 = time.time()
        try:
            resp = _post(body)
            raw = resp["choices"][0]["message"]["content"] or ""
            rec.update(reply=raw, usage=resp.get("usage"), latency_s=round(time.time() - t0, 2))
            data = _parse(raw)
            rec["rationale"] = data.get("rationale")
            _log(rec)
            break
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:2000]
            rec.update(error=f"HTTP {e.code}", detail=detail)
            _log(rec)
            if e.code == 400 and structured and "response_format" in detail.lower():
                structured = False          # model can't do json_schema: ask in plain text
                continue
            if e.code != 429 and e.code < 500:
                raise AdvisorError(f"HTTP {e.code}: {detail[:300]}") from None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError,
                AdvisorError, KeyError, IndexError) as e:
            rec["error"] = repr(e)
            _log(rec)
            if isinstance(e, AdvisorError) and "OPENROUTER_API_KEY" in str(e):
                raise
        if attempt < retries:
            time.sleep(2 ** attempt)
    else:
        raise AdvisorError(f"no usable reply after {retries + 1} attempts")

    seen = {_key(h["params"], space) for h in history}
    out = []
    for c in data.get("candidates", []):
        try:
            fixed = {p.name: p.fix(c[p.name]) for p in space}
        except (KeyError, TypeError, ValueError):
            continue
        k = _key(fixed, space)
        if k not in seen:
            seen.add(k)
            out.append(fixed)
    return out[:n]
