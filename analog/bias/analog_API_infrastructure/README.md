# Analog API Infrastructure: LLM-Assisted Neuron Sizing

Python tooling that uses language models on [OpenRouter](https://openrouter.ai)
to propose device sizes, bias voltages and testbench settings for the analog
integrate-and-fire neuron (`analog/neuron/`, based on Fig. 4 of Indiveri et
al. 2011), then checks each proposal against a target spec by running ngspice.

> **Status:** the loop runs end to end with the random proposer (milestones
> 1–5, plus the milestone 8 comparison script). `advisor.py` is complete and
> tested against stubbed API replies; no real OpenRouter call has been made yet
> (milestone 6). The user's original draft is kept as `advisor_draft.py`.
> See [Quick start](#quick-start).

> **This copy** (`analog/bias/analog_API_infrastructure/`) is the team's
> `tools/analog_API_infrastructure/`, plus the changes used to size the bias
> generator: an `evaluator` option in `sim.yaml`, a `--proposer grid`, and
> `configs_bias/`. The original folder is unchanged. Run it from this folder in
> the same way. `configs_bias` calls `analog/bias/sim/sweep_point.py`, which is
> not in this branch.

## Quick start

Run inside the iic-osic-tools container, from this folder:

```bash
python3 loop.py --proposer random --budget 20      # baseline, no API needed
python3 loop.py --proposer llm --model <slug> --budget 20
python3 compare.py                                 # table of all runs in runs/
```

| File | Role |
|---|---|
| `configs/params.yaml` | tunable parameters: `lo`, `hi`, `step`, `init`, and `devices` (netlist fields the parameter sets, `subckt/INSTANCE:field`) |
| `configs/spec.yaml` | targets, `[min, max]`, `null` = unbounded |
| `configs/sim.yaml` | testbench `.sch`, fixed `.param` values, analysis/`.meas` block, timeout, constraints |
| `params.py` | loads the three YAML files (`Param`, `Spec`) |
| `netlist.py` | netlists the testbench with xschem once, builds `template.spice` (drops `.control`, overridden `.param`s; device fields → `{PARAM}`), writes `params.spice` |
| `runner.py` | `ngspice -b` in a per-point folder with a timeout (`num_threads=1`) |
| `metrics.py` | `parse_meas`, `area`, `meets_spec`, `score` |
| `advisor.py` | OpenRouter client: prompt, `json_schema` structured output (plain-JSON fallback), retries with backoff on 429/5xx, clamp/snap, de-duplication; logs every prompt/reply/token count to the run's `advisor_log.jsonl` |
| `advisor_draft.py` | the user's original draft, kept unchanged for reference; not imported |
| `loop.py` | propose → validate → simulate (parallel) → log; random proposer built in, LLM proposer calls `advisor.suggest()` |
| `compare.py` | sims to first pass and best score per run |

The schematic doesn't need editing: device sizes are replaced in the netlist
template, so step 3 below is optional. The `init` point (the hand-sized 5 kHz
design) is simulated first in every run as a reference, even if it is over the
area budget. For `--proposer llm`, set `OPENROUTER_API_KEY` (and optionally
`ADVISOR_MODEL`) in the container shell; `advisor.py` uses only the Python
standard library, so nothing needs installing.

### Other blocks: `evaluator` and the grid proposer

A block whose metrics need many simulations (calibration, corners, Monte Carlo) can
use an evaluator script instead of a testbench. In `sim.yaml`, set
`evaluator: <script>` (repo-relative) and `evaluator_args`. For each point the loop
runs `python3 <script> --params params.json --dir pNNNN` and reads its
`name = value` lines like `.meas` output.

`--proposer grid` simulates every lo, lo+step, …, hi combination that passes the
`constraints`.

`configs_bias/` sizes the unit mirror device of the bias generator (`analog/bias`).
Each point runs `analog/bias/sim/sweep_point.py`, and
`analog/bias/sim/sweep_report.py` summarizes the run:

```bash
python3 loop.py --configs configs_bias --proposer grid --budget 40 --batch 2 --jobs 2 --keep-going
python3 ../sim/sweep_report.py   # not in this branch
```

---

## 1. How it works

```
spec.yaml + params.yaml
          │
          ▼
┌──────────────┐  candidates (JSON)  ┌──────────────┐   rejects: out of bounds,
│  advisor.py  │ ──────────────────▶ │  validate    │   over area budget,
│ (OpenRouter) │                     │  (Python)    │   duplicates
└──────────────┘                     └──────┬───────┘
       ▲                                    │ valid candidates
       │ history table                      ▼
       │ (params → metrics)          ┌──────────────┐
       │                             │  netlist.py  │  writes .param values
       │                             └──────┬───────┘  into a template netlist
       │                                    ▼
       │                             ┌──────────────┐
       │                             │  runner.py   │  ngspice -b (batch)
       │                             └──────┬───────┘
       │                                    ▼
       │                             ┌──────────────┐
       └──────────────────────────── │  metrics.py  │  parses .meas results +
                                     └──────────────┘  computes area in Python
```

The loop is: **propose → validate → simulate → measure → log → repeat**,
until a candidate meets every spec or the iteration/budget limit is reached.

**Ground rule:** the LLM only *proposes*. Python enforces every bound and
constraint, and ngspice decides whether a design meets spec. No number from
the model is used without being clamped, checked and simulated.

---

## 2. What you control

### 2.1 Spec: targets that a design must meet (`spec.yaml`)

| Metric | Symbol | How it is obtained | Example target |
|---|---|---|---|
| Spike frequency at a reference input current | `f_spike` | `.meas`: 1 / time between consecutive spikes, constant DC input | 50–200 Hz at 1 nA |
| Spike width | `t_spike` | `.meas`: time `spike` stays above VDD/2 | 0.5–2 ms |
| Reset (down-swing) time | `t_reset` | `.meas`: from the Vmem peak to Vmem < 10% VDD | < 100 µs |
| Refractory time | `t_refr` | `.meas`: from the end of reset to Vmem rising again, with input still on | 1–5 ms |
| Firing threshold | `v_thr_eff` | `.meas`: Vmem when `spike` rises | close to VT |
| Average power | `p_avg` | `.meas`: average of −i(V1)·VDD over the run | < 50 nW |
| Active (transistor) area | `a_active` | **Python**: Σ W·L over all transistors × layout factor | < 400 µm² |
| Capacitor area | `a_cap` | **Python**: Σ W·L over all MIM capacitors | < 700 µm² |

Area metrics need no simulation. Check them **before** calling ngspice so
over-budget candidates are rejected cheaply.

Suggested format:

```yaml
# spec.yaml: [min, max] in SI units; null = unbounded
f_spike:  [50, 200]        # Hz, at i_ref below
t_reset:  [null, 100e-6]   # s
t_refr:   [1e-3, 5e-3]     # s
a_active: [null, 400e-12]  # m^2
a_cap:    [null, 700e-12]  # m^2
conditions:
  i_ref: 1e-9              # A, DC input used for f_spike
```

### 2.2 Parameters: what the optimizer may change (`params.yaml`)

| Group | Parameters | Notes |
|---|---|---|
| Capacitors | `W_C2`, `L_C2` (C_mem), `W_C1`, `L_C1` (C_K) | `cap_mim_2f0_*` ≈ 2 fF/µm². Respect the PDK minimum MIM size. |
| Bias voltages | `Vlk`, `VNA`, `VK`, `VIp`, `VKup`, `VKdn`, `Vamp_bias`, `VT` | Sources already exist in `neuron_testbench.sch`. In subthreshold, the current changes ~10× per ~80–100 mV, so use mV steps. |
| Transistor sizes | `W_Mx`, `L_Mx`, grouped | Group devices that must match (e.g. both inverters) so the search space stays small. |
| Stimulus | `ipk`, `pulse_width`, `per` | Usually fixed by the spec, not optimized. |

Each parameter needs `lo`, `hi` and `step`. That is what `Param` in
`advisor.py` is for:

```yaml
# params.yaml
VKdn:  {lo: 0.20,  hi: 0.60,  step: 0.005}   # V
W_C2:  {lo: 5e-6,  hi: 30e-6, step: 0.5e-6}  # m
```

**Start small:** optimize 3–5 parameters (e.g. `W_C2`, `W_C1`, `VKup`, `VKdn`,
`VNA`) with transistor sizes fixed. Widen the space only once the loop works.

---

## 3. Preparing the schematic for automation

1. **Make every tunable a parameter.** In xschem, set device fields to
   `W=\{W_C2\}`, `L=\{L_C2\}`, etc. The bias sources already use `\{VKdn\}` and
   similar. Note that these bias parameters are currently **not defined** in
   the testbench's `.param` line, so the current testbench won't run until
   they are.
2. **Add a separate code block for automation.** Keep the interactive
   TRAN_SIM block (with `plot`) for manual use and disable it with
   `spice_ignore=true` for automated runs. The automation block should contain:
   - `.include` of a generated `params.spice` file (the only file Python writes);
   - `.tran` and `.meas` statements (dot commands, not inside `.control`), so
     results print to the batch log as `name = value`;
   - **no** `plot` and no absolute `write` paths.
3. **Netlist once, then reuse it.** Generate the netlist from xschem (GUI
   *Netlist*, or command line: see `xschem --help` for the batch-netlist
   flags). Python then changes only `params.spice` between runs, so xschem is
   not needed inside the loop.
4. **Where it runs:** ngspice and the GF180 models live in the course
   container (`/foss/designs` = `~/eda/designs`). Run the Python loop
   **inside the container**, and check that the container can reach
   `openrouter.ai`.

Example `.meas` lines (define edges on `spike`, which rises at firing):

```spice
.meas tran t1  WHEN v(spike)=1.65 RISE=2
.meas tran t2  WHEN v(spike)=1.65 RISE=3
.meas tran f_spike PARAM='1/(t2-t1)'
.meas tran t_spike TRIG v(spike) VAL=1.65 RISE=2 TARG v(spike) VAL=1.65 FALL=2
.meas tran i_avg AVG i(V1) FROM=1m TO=10m
.meas tran p_avg PARAM='-i_avg*3.3'
```

Skip the first spike (`RISE=2`, `RISE=3`), because the first period starts
from the initial condition. Treat a failed `.meas` (no spikes) as a metric
value of `None`, not as an error.

---

## 4. Suggested module layout

```
tools/analog_API_infrastructure/
├── README.md          ← this file
├── advisor.py         ← OpenRouter client: build prompt, call API, parse JSON
├── params.py          ← load params.yaml / spec.yaml → Param objects, Spec
├── netlist.py         ← write params.spice from a dict of values
├── runner.py          ← run ngspice in batch mode with a timeout; return log text
├── metrics.py         ← parse .meas lines; compute a_active / a_cap in Python
├── loop.py            ← main loop: propose → validate → simulate → log
├── configs/
│   ├── spec.yaml
│   └── params.yaml
└── runs/              ← one folder per run (gitignored)
    └── <timestamp>/
        ├── history.jsonl    ← one line per simulated point
        └── advisor_log.jsonl← prompts, raw model replies, model slug, tokens
```

Suggested interfaces. Write the bodies yourself:

| Function | Input → Output |
|---|---|
| `load_space(path) -> list[Param]` | YAML → parameter definitions |
| `load_spec(path) -> Spec` | YAML → `{metric: (lo, hi)}` |
| `area(values) -> dict` | parameter values → `{"a_active": …, "a_cap": …}` |
| `write_params(values, path)` | dict → `.param name=value` lines |
| `run_ngspice(netlist, workdir, timeout) -> str` | run → log text (raise on timeout) |
| `parse_meas(log) -> dict` | log text → `{name: float | None}` |
| `meets_spec(metrics, spec) -> bool` | all metrics within `[lo, hi]` |
| `score(metrics, spec) -> float` | how far from spec (0 = meets it), for ranking |
| `propose(space, history, spec, n) -> list[dict]` | API call → candidate list |

---

## 5. The OpenRouter call

- **Endpoint:** `POST https://openrouter.ai/api/v1/chat/completions`. The API
  is OpenAI-compatible, so `requests` or the `openai` package (with `base_url`)
  both work.
- **API key:** read it from the environment (`OPENROUTER_API_KEY`). Never put
  it in code or in git; add `.env` to `.gitignore`.
- **Model:** pass the exact slug from openrouter.ai/models (`ADVISOR_MODEL`).
  Log the slug with every call, so results can be reproduced and compared
  across models.
- **Structured output:** send `response_format = {"type": "json_schema",
  "json_schema": _schema(space)}`. Not every model supports it, so check the
  model's page and keep a fallback: parse JSON from plain text, then retry
  once if that fails.
- **What the prompt contains:**
  1. the system prompt: the role, plus "respond only with JSON";
  2. the parameter table: name, unit, lo, hi, step;
  3. the spec table;
  4. the history: params → metrics for every point simulated so far
     (truncate to the best *k* plus the most recent *m* when it gets long);
  5. the number of candidates wanted.
- **Robustness:** set a timeout; retry with backoff on HTTP 429/5xx; cap the
  calls per run; record the token usage the response returns.

---

## 6. Validation (Python, before simulating)

For each candidate:
1. Clamp it to `[lo, hi]` and snap it to `step`: that is `Param.fix`.
2. Reject it if it's identical to a point already simulated: that is `_key`.
3. Reject it if `area(...)` is over budget, and log the reason.
4. Optionally reject physically meaningless combinations, e.g. `VKdn` above
   `VKup` if refractory time must be longer than spike width.

Log rejected candidates too. How often the model proposes invalid points is
useful data for your report.

---

## 7. Baseline and evaluation

Implement a **random-search** or **grid** proposer with the same interface as
`propose()`. Run both with the same simulation budget and compare:
- the number of simulations until the spec is first met;
- the best score after N simulations;
- API cost and wall-clock time.

Without this baseline you can't show that the LLM helps.

---

## 8. Fixing `advisor.py` (historical: applies to `advisor_draft.py`)

These bugs in the current draft stop it from importing or working:

| Location | Problem | What it should do |
|---|---|---|
| `LOG_PATH = …` | `os.enrivon` | `os.environ` |
| `Param.fix` | uses undefined `s`; brackets in the wrong place | number of steps from `lo` = `round((x - lo) / step)` |
| `Spec = …` | `tuple{float,float]` is a syntax error | `tuple[float, float]` |
| `meets_spec` | body is a copy of `_key` (uses undefined `params`, `space`) | return whether every spec metric is present, not `None`, and within `[lo, hi]` |
| `_schema` | `{"type","string"}` is a **set**, not a dict (same for `"array"`) | `{"type": "string"}`, `{"type": "array", "items": …}` |
| `_schema` | missing comma after the `"properties"` dict | add `,` |
| `SYSTEM_PROMPT` | typos ("simualted", "saprse", "wiht") and leading spaces | clean up; typos in prompts can slightly change model behaviour |
| imports | `random`, `time`, `json` unused so far | keep them for retry/backoff and logging |

---

## 9. Milestones

Build in this order. Each step has a check that tells you it works.

| # | Step | Done when |
|---|---|---|
| 1 | Fix `advisor.py` so it imports | `python -c "import advisor"` succeeds |
| 2 | Parameterize the schematic and add the automation code block | a hand-edited `params.spice` + `ngspice -b` prints all `.meas` values |
| 3 | `runner.py` + `parse_meas` | one Python call returns a metrics dict for the current design |
| 4 | `area()` | numbers match a hand calculation for the current schematic |
| 5 | Random-search loop (no API yet) | 10 random points simulated and logged to `history.jsonl` |
| 6 | `propose()` with OpenRouter | one API call returns valid, schema-conforming candidates |
| 7 | Full LLM loop | the loop runs to a budget and stops early on the first point that meets spec |
| 8 | Compare with the baseline | table/plot of LLM vs random for the same budget |
| 9 | (optional) More robust results | re-simulate the final design at ss/ff corners and several temperatures |

---

## 10. Notes

- **Units:** SI everywhere in the code (m, V, A, s, F). Convert only for display.
- **Reproducibility:** each run folder stores the configs, the model slug, the
  netlist template hash and every prompt/response pair.
- **Simulation time:** spike-rate measurements need several periods. Keep
  `tran` as short as possible (e.g. 3–4 periods) and set a sensible maximum
  step.
- **AI-usage record:** this README was drafted with AI assistance; see
  `analog/Analog_AI_Documentation.md`. `params.py`, `netlist.py`, `runner.py`,
  `metrics.py`, `loop.py`, `compare.py`, `configs/` and `advisor.py` were
  written by the AI at the user's request (2026-11-04). `advisor_draft.py` is
  the user's own draft, renamed but not edited.
