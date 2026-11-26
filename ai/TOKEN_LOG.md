# Token cost log: AI-assisted gLayout work

Tracks what each AI-driven layout task cost in tokens, to compare against hand layout and
to see which helpers pay off.

**How the numbers are made.** The assistant cannot read its own token meter, so figures
are **estimates**: characters ÷ 4 of what was written (output) and what tool results
returned (input). Two costs are *not* in the per-step numbers:
- **Reasoning tokens** (the assistant's internal planning): not measurable here; given as a
  rough range per task.
- **Context re-reads**: every turn re-sends the whole conversation (mostly prompt-cached,
  so cheaper per token but large in count). This grows with session length and is usually
  the biggest real cost; keeping sessions short and outputs compact is what reduces it.

---

## Task 1: spike amplifier layout (`gen_spike_amp.py`), 2026-11-15

Result: **DRC clean + LVS match on the first full run** (42.8 × 46.7 µm, 5 devices,
24 dummies, shared DNW). One geometry bug was caught by inspecting `describe()` output
*before* running DRC.

| # | Step | Output tok (est.) | Input tok (est.) | Notes |
|---|------|------------------:|-----------------:|-------|
| 1 | Probe FET bus positions (2 small scripts) | 400 | 500 | needed to plan routing; `bus()` would make this a one-liner next time |
| 2 | Write `gen_spike_amp.py` | 2,100 | — | 8.3 kB file |
| 3 | Build + `describe()` | 50 | 500 | spotted PMOS gate bar not reaching net2 riser |
| 4 | Fix gate bar (1 edit) | 150 | 50 | |
| 5 | DRC + LVS script and run | 300 | 100 | ~45 s wall time; output filtered to 4 lines |
| 6 | Verify extracted netlist topology | 150 | 400 | guards against "LVS match" on wrong reference |
| 7 | Schematic consistency check (git diff, nets) | 150 | 900 | found M3 already 0.5/0.64; found VN wire gap |
| 8 | This log | 900 | — | |
| | **Subtotal (measured-ish)** | **≈4,200** | **≈2,450** | |
| | Reasoning (rough) | 6,000–10,000 | | routing plan, layer assignment, spacing checks |

### What kept it cheap
- **Helpers did the rule-heavy work.** `dummy_ring` / `dnw_guard` / `nwell_guard` were
  already DRC/LVS-verified, so no DRC repair loops this time. Developing those helpers
  took 4 DRC/LVS iterations (estimated 15–20k tokens incl. reasoning); that cost is
  now amortised over every cell that uses them.
- **Filtered tool output.** DRC/LVS logs were grepped to 2–4 lines; a raw KLayout log is
  several thousand tokens.
- **No port dumps.** A single glayout FET has ~800 ports; listing them would cost ~8k
  tokens. Direct bus lookups (`multiplier_0_<term>_E/W`) avoided it.

### What cost more than needed
- Step 1 (probing bus geometry) is repeated work; a `bus(dev, term)` helper now lives in
  `gen_spike_amp.py` and could move into `glayout_helpers.py`.
- Hand-placed wire coordinates (offsets like `±0.8`, `±2.5`) needed reasoning about
  neighbouring vias; a small router that keeps a per-layer occupancy list would remove
  most of it.

---

## Task 2: full neuron layout (`gen_neuron_glayout.py` + `glayout_router.py`), 2026-11-15

Result: **DRC clean + LVS match after 3 DRC/LVS runs**. 98.7 × 62.0 µm; 17 transistors
(12 neuron + 5 spike amp, flattened), 2 MIM caps (0.98 pF, 0.20 pF), 120 dummies, one
shared DNW. New: a row/channel router with a built-in short/spacing checker.

| # | Step | Output tok (est.) | Input tok (est.) | Notes |
|---|------|------------------:|-----------------:|-------|
| 1 | Read schematic, old LVS ref, old generator header | 100 | 1,500 | found the old layout uses pre-sizing devices |
| 2 | xschem netlist + MIM cap probe | 200 | **6,500** | **waste: full port dump of mimcap (~6k)**; should have used `ports_brief` |
| 3 | Write `glayout_router.py` | 1,400 | — | Router + checker + track packer |
| 4 | Write `gen_neuron_glayout.py` | 2,800 | — | |
| 5 | Run 1 → router check | 50 | 150 | **checker caught 2 shorts + 2 spacing errors before DRC** |
| 6 | PMOS-row shift (naive) → infeasible | 300 | 100 | |
| 7 | Rewrite as track-aware plan (order tracks + shift search) | 1,200 | 400 | |
| 8 | Tidy + DRC/LVS run 1 | 400 | 100 | DRC clean first time; LVS fail |
| 9 | LVS diff | 100 | **2,500** | **waste: printed ~70 dummy lines; filter them next time** |
| 10 | Fix MIM tab short + VDD label | 700 | 300 | glayout MIM tab lifts bottom plate to met5 |
| 11 | DRC/LVS run 2 + MIMTM.1 rule lookup | 150 | 1,400 | MIM bottom plate needs 1.2 µm to other met4 |
| 12 | Fix split VDD columns + cap gap; run 3 | 700 | 100 | DRC clean, LVS match |
| 13 | Topology verification | 100 | 800 | |
| 14 | This log | 1,000 | — | |
| | **Subtotal (measured-ish)** | **≈9,200** | **≈13,850** | ~9k of the input was avoidable dumps |
| | Reasoning (rough) | 25,000–40,000 | | floorplan, router design, riser-conflict model |

### What kept it cheap
- **Router pre-check** (`Router.check()`): every shape is tagged with its net, so shorts
  print as one line (`met3 SHORT: net5[M7.D] vs net1[A5.D]`) in < 1 s instead of a
  ~1 min DRC/LVS run plus reading a netlist diff. It caught 4 errors before the first DRC.
- **Fixed layer plan** (met3 vertical, met4 horizontal, met5 caps) makes most crossings
  legal by construction, so the planner only has to reason about same-layer conflicts.
- **Verified helpers reused**: dummy rings + DNW/n-tap guards needed zero fixes.

### What cost more than needed
- Two avoidable dumps (~9k input tokens, ~65 % of all input): the MIM cap port list and an
  unfiltered LVS netlist. Rule for next time: `ports_brief()` for any new primitive, and
  always filter dummy lines out of extracted netlists.
- The first PMOS-shift idea was too strict (any x-overlap); one extra iteration before
  modelling the real condition (NMOS track ≥ PMOS track at the same x).
- Two glayout MIM-cap surprises (met5 on the bottom-plate tab; MIMTM.1 1.2 µm) cost one
  DRC/LVS round each. Both are now recorded in memory and in the generator comments.

---

## Task 3: PEX + testbench of the gLayout neuron, 2026-11-15

Result: Magic RC extraction (existing `PEX/extract.sh`) + `neuron_sized_testbench` stimulus
(9.5 nA, 1.6 ms). Post-layout neuron fires regularly; period 237.3 µs vs 208.6 µs
pre-layout (+13.8 %).

| # | Step | Output tok (est.) | Input tok (est.) | Notes |
|---|------|------------------:|-----------------:|-------|
| 1 | Read PEX scripts, wrapper tool, testbench | 100 | 1,700 | reused the existing flow |
| 2 | Extraction (`extract.sh`) | 50 | 250 | 1 s; wrapper step needs a .sym |
| 3 | Hand-written wrapper (1 failed parse, then reuse `symbol_pins`) | 900 | 300 | |
| 4 | Netlist testbench, build 3 decks | 700 | 900 | A schematic / B pre-layout / C post-layout |
| 5 | Run sims (parallel), read results | 100 | 450 | C hit 1.9 GB (`save all` x 5k nodes) |
| 6 | Re-run C with 2 saved vectors | 100 | 150 | 7.3 min wall |
| 7 | Parse raw files for all spike times | 700 | 400 | avoided a 2nd 7-min sim for the period |
| 8 | Parasitic-C breakdown + "B + C_par" diagnostic sim | 700 | 400 | explains ~half of the shift |
| 9 | This log | 700 | — | |
| | **Subtotal (measured-ish)** | **≈4,050** | **≈4,550** | |
| | Reasoning (rough) | 8,000–12,000 | | |

Lessons: save only the vectors the measurements use in any PEX transient (memory and
runtime scale with node count); parse the .raw instead of re-simulating for a new metric.

---

## Task 4: prediction infrastructure (`glayout_predrc.py`, `glayout_parasitics.py`), 2026-11-15

Result: DRC predictor (20 checks, 0.1 s) agrees with the real deck on 4/4 layouts
(clean, 2 known-bad mutations, 1 near-miss). Parasitic predictor (Magic tech coefficients
on router shapes, 0.1 s) is within 2–25 % per net before calibration; with calibration the
predicted-C pre-layout sim (80 s) gives a period within **+1.1 %** of full PEX (7.3 min).

| # | Step | Output tok (est.) | Input tok (est.) | Notes |
|---|------|------------------:|-----------------:|-------|
| 1 | Find tools + Magic cap coefficients + real rule formulations | 300 | 2,600 | deck grep was the big input |
| 2 | Write `glayout_predrc.py` | 2,200 | — | |
| 3 | Mutation tests (4 layouts) + real DRC on each | 600 | 400 | the proof the predictor is trustworthy |
| 4 | Write `glayout_parasitics.py` | 2,600 | — | |
| 5 | Register device buses, compare with PEX | 700 | 600 | |
| 6 | Calibrate + inject + sim (found top-level-node bug, fixed) | 1,000 | 600 | |
| 7 | Wire both into the generator | 500 | 400 | |
| 8 | This log | 600 | — | |
| | **Subtotal (measured-ish)** | **≈8,500** | **≈4,600** | |
| | Reasoning (rough) | 15,000–25,000 | | |

Expected payback: each avoided DRC/LVS loop was ≈3–4k tokens + ~1 min; each avoided
full PEX sim ≈7 min. The neuron needed 2 such loops and 1 PEX sim.

---

## Task 5: parser, reusable floorplan, decision engine, 2026-11-15

Result: `glayout_netlist.py` (schematic -> flat table, finds the VN bug by itself),
`glayout_floorplan.py` (two_row + CLI; neuron generator 350 -> 40 lines; spike amp built
from the CLI with no code, 17 % smaller than the hand version), `decide.py` +
`layout_policy.yaml` (wells / dummies / rings / placement with reasons and questions).
Neuron rebuilt from the floorplan and again from decisions: DRC clean + LVS match each time
(first try). Corner characterization started (results pending).

| # | Step | Output tok (est.) | Input tok (est.) | Notes |
|---|------|------------------:|-----------------:|-------|
| 1 | Parser + 2 fixes (quoted params, x prefix) | 3,300 | 1,200 | |
| 2 | Floorplan module + thin generator + CLI | 5,500 | 4,500 | read the 350-line generator once to move it |
| 3 | DRC/LVS of neuron + CLI spike amp | 300 | 150 | both clean first try |
| 4 | Corner module + decks + launch | 3,500 | 600 | |
| 5 | Parser on 4 other cells -> generalization plan | 300 | 900 | |
| 6 | Parser bus/global fixes, policy, decide.py | 6,500 | 1,500 | |
| 7 | 3 rule fixes found by running on DAC/neuron | 1,200 | 1,800 | |
| 8 | Decision-driven neuron, DRC/LVS | 200 | 400 | clean first try |
| | **Subtotal (measured-ish)** | **≈20,800** | **≈11,050** | |
| | Reasoning (rough) | 25,000–40,000 | | |

A new two_row cell now costs: one `decide.py` run, answering its questions in YAML, one
`glayout_floorplan.py --decisions` run, one signoff. Expected ≈1–3k tokens if nothing new
breaks, vs ≈23k for the neuron the first time.

---

## Task 6: extraction feedback + file-based flow for API use, 2026-11-15

Result: per-cell calibration store with history (`parasitic_calib.json` v2, migrated);
`flow.py` stages (table/decide/answer/build/signoff/sim/status/run) with JSON artifacts in
flow/<cell>/; `flow_cells.yaml` registry; `AGENT_BRIEF.md` (~900 tokens, replaces the chat
as context); `api_driver.py` (tool runner, 3 restricted tools, prints measured usage —
**not run yet**: SDK not installed, paid calls need approval). Neuron end to end through
`flow.py run`: 90 s, DRC clean, LVS match, calibration fed back (10 nets, factor 1.117).

| # | Step | Output tok (est.) | Input tok (est.) |
|---|------|------------------:|-----------------:|
| 1 | Calibration store v2 + feedback | 2,200 | 900 |
| 2 | build.json / shapes export | 700 | 100 |
| 3 | flow.py + registry + answer stage | 5,200 | 900 |
| 4 | Read SDK docs (tool runner), brief, driver | 3,000 | 2,500 |
| 5 | End-to-end runs (neuron, DAC) + this log | 800 | 900 |
| | **Subtotal** | **≈11,900** | **≈5,300** |
| | Reasoning (rough) | 10,000–15,000 | |

Context for a future API call: brief (~900) + status (~150) + request, vs this session's
context of well over 100k tokens.

---

## Running totals

| Task | Output tok | Input tok | Reasoning (rough) | DRC/LVS iterations |
|------|-----------:|----------:|------------------:|-------------------:|
| Ring helpers (`glayout_rings.py`), 2026-11-15 | ≈7,000 | ≈9,000 | 15k–20k | 4 |
| Spike amp layout, 2026-11-15 | ≈4,200 | ≈2,450 | 6k–10k | 1 |
| Neuron layout + router, 2026-11-15 | ≈9,200 | ≈13,850 | 25k–40k | 3 |
| Neuron PEX + testbench, 2026-11-15 | ≈4,050 | ≈4,550 | 8k–12k | — (4 sims) |
| Prediction infrastructure, 2026-11-15 | ≈8,500 | ≈4,600 | 15k–25k | 4 DRC (validation) |
| Parser + floorplan + decisions, 2026-11-15 | ≈20,800 | ≈11,050 | 25k–40k | 3 (all clean first try) |
| Feedback + flow.py + API structure, 2026-11-15 | ≈11,900 | ≈5,300 | 10k–15k | 1 (clean) |

*Add a row per task. Keep the method the same so rows stay comparable.*
