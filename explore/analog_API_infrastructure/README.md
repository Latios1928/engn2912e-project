# analog_API_infrastructure/

LLM-assisted sizing loop used for the neuron: a model on [OpenRouter](https://openrouter.ai)
proposes device sizes and bias voltages, Python checks every bound and the area budget, and ngspice
decides whether a design meets the spec (propose → validate → simulate → measure → log). Design
notes: [`ai/analog_API_infrastructure_design.md`](../../ai/analog_API_infrastructure_design.md).

## Running

Inside the container, from this folder:

```bash
python3 loop.py --proposer random --budget 20      # baseline, no API needed
python3 loop.py --proposer llm --model <slug> --budget 20
python3 compare.py                                 # table of all runs in runs/
```

For `--proposer llm`, set `OPENROUTER_API_KEY` (and optionally `ADVISOR_MODEL`). `advisor.py` uses
only the Python standard library. Each run gets `runs/<timestamp>_<proposer>/` (git-ignored) with
the configs, `history.jsonl` (one line per simulated point) and `advisor_log.jsonl` (prompts,
replies, token counts). The `init` point (the hand-sized design) is simulated first as a reference.

| File | Role |
|---|---|
| `configs_sized/params.yaml` | tunable parameters: `lo`, `hi`, `step`, `init`, and `devices` (netlist fields the parameter sets, `subckt/INSTANCE:field`) |
| `configs_sized/spec.yaml` | targets, `[min, max]`, `null` = unbounded |
| `configs_sized/sim.yaml` | testbench `.sch`, fixed `.param` values, analysis / `.meas` block, timeout, constraints |
| `loop.py` | the loop (default `--configs configs_sized`) |
| `advisor.py` | OpenRouter client; `advisor_draft.py` is the original draft, kept unchanged and not imported |
| `params.py`, `netlist.py`, `runner.py`, `metrics.py`, `compare.py` | config loading, netlist template, ngspice runs, measurements, run comparison |
