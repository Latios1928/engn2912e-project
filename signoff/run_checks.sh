#!/bin/bash
# Re-run the chip signoff checks on the published chip (gds/snn_top.gds, verilog/gl/snn_top.v,
# librelane/snn_top/results/) and collect the results into signoff/results/ and signoff/img/.
#
#   signoff/run_checks.sh             full-chip LVS + digital gate-level tests (about 5 min)
#   signoff/run_checks.sh --spice     also the post-layout mixed-signal run, scenarios 1-8 (+11 min)
#   signoff/run_checks.sh --collect   re-run nothing; collect from the last outputs
#
# Each check's own tool writes its full log where it always does (gitignored); this script
# keeps the lines that carry the verdict, with the date and commit, in signoff/results/*.txt.
# Exits non-zero if any check fails or has no output.
set -u
cd "$(dirname "$0")/.."
ROOT=$(pwd)
OUT=$ROOT/signoff/results
IMG=$ROOT/signoff/img
export PATH=/foss/tools/bin:$PATH
mkdir -p "$OUT" "$IMG"

RUN=1 SPICE=0
case "${1:-}" in
  --spice) SPICE=1 ;;
  --collect) RUN=0 ;;
  "") ;;
  *) sed -n '2,12p' "$0"; exit 2 ;;
esac

REV="$(git rev-parse --short HEAD)$(git diff --quiet HEAD -- gds verilog librelane analog/layout_tools \
      mixed || echo ' (with uncommitted changes)')"
STATUS=()

# header <file> <title> <source>: the source's date is its last commit if git tracks it
# (a checkout resets the file time), else the time the tool wrote it
header() {
  local when
  if git ls-files --error-unmatch "$3" > /dev/null 2>&1; then
    when="committed $(git log -1 --format=%cd --date=format:'%F %H:%M' -- "$3")"
  else
    when="written $(date -r "$ROOT/$3" '+%F %H:%M' 2>/dev/null || echo '?')"
  fi
  { echo "# $2"
    echo "# source: $3 ($when)"
    echo "# collected $(date '+%F %H:%M') at commit $REV"
    echo; } > "$1"
}

# verdict <name> <file> <pass regex> <fail regex>
verdict() {
  if [ ! -s "$2" ] || ! grep -qE "$3" "$2" || grep -qE "$4" "$2"; then
    STATUS+=("FAIL  $1"); return 1
  fi
  STATUS+=("PASS  $1")
}

# ---- 1. full-chip LVS down to transistors, plus the build-chain checks
if [ $RUN = 1 ]; then
  echo "== chip_lvs.py (about 2 min)"
  python3 librelane/snn_top/chip_lvs.py > /dev/null 2>&1
fi
F=$OUT/chip_lvs.txt
header "$F" "Full-chip LVS (Magic extraction + netgen) and build-chain checks" librelane/snn_top/chip_lvs/summary.txt
cat librelane/snn_top/chip_lvs/summary.txt >> "$F" 2>/dev/null
verdict "full-chip LVS and build chain (chip_lvs.py)" "$F" "Circuits match uniquely" "^FAIL"

# ---- 2. digital gate-level simulations
if [ $RUN = 1 ]; then
  echo "== gls: make, make timing (about 3 min)"
  make -C librelane/snn_top/gls > /dev/null 2>&1
  make -C librelane/snn_top/gls timing > /dev/null 2>&1
fi
F=$OUT/gls.txt
header "$F" "Gate-level simulation, behavioral analog model (mock/tb_snn_top.v)" librelane/snn_top/gls/gls.log
grep -E "PASS|FAIL|ERROR" librelane/snn_top/gls/gls.log >> "$F" 2>/dev/null
verdict "gate-level, behavioral analog (gls: make)" "$F" "PASS: snn_top" "FAIL|ERROR"

F=$OUT/gls_timing.txt
header "$F" "Gate-level timing simulation at 1 MHz, zero-delay and SDF corners (gls/tb_gls_timing.v)" \
  librelane/snn_top/gls/timing_zero.log
for log in librelane/snn_top/gls/timing_zero.log librelane/snn_top/gls/timing_nom_*.log; do
  [ -f "$log" ] || continue
  case $log in *.compile.log) continue ;; esac
  c=$(basename "$log" .log); c=${c#timing_}
  echo "## $c" >> "$F"
  grep -E '^tb_gls_timing: ' "$log" | sed "s|$ROOT/||" >> "$F"
done
n_pass=$(grep -c '^tb_gls_timing: PASS' "$F")
if [ "$n_pass" -eq 4 ]; then
  verdict "gate-level timing, zero-delay + ss/tt/ff SDF (gls: make timing)" "$F" "PASS" "FAIL"
else
  STATUS+=("FAIL  gate-level timing: $n_pass of 4 runs (zero-delay + 3 SDF corners) passed")
fi

# ---- 3. mixed-signal gate-level: netlist in Icarus, analog macro (post-layout) in ngspice
if [ $SPICE = 1 ]; then
  echo "== gls_ms: make run PEX=1 (about 11 min)"
  make -C librelane/snn_top/gls_ms run PEX=1 > /dev/null 2>&1
fi
for v in gls_ms_pex gls_ms; do
  log=librelane/snn_top/gls_ms/$v.log
  [ -f "$log" ] || continue
  F=$OUT/$v.txt
  if [ $v = gls_ms_pex ]; then what="post-layout macro (extracted parasitics)"; else what="schematic macro"; fi
  header "$F" "Mixed-signal gate-level simulation, $what, scenarios 1-8" "${log#$ROOT/}"
  head -1 "$log" | sed "s|$ROOT/||g" >> "$F"
  tr '\r' '\n' < "$log" | grep -E '^snn_ms_tb: ' | awk '!seen[$0]++' >> "$F"
  raw=librelane/snn_top/gls_ms/$v.raw
  if [ -f "$raw" ]; then
    echo >> "$F"; echo "## spike summary (tools/snn_waves.py)" >> "$F"
    title="Gate-level + SPICE, post-layout macro"; [ $v = gls_ms ] && title="Gate-level + SPICE, schematic macro"
    python3 tools/snn_waves.py "$raw" -o "$IMG/$v" --title "$title" 2>&1 | sed "s|$ROOT/||g" >> "$F"
  fi
  verdict "mixed-signal gate-level, $what ($v)" "$F" "snn_ms_tb: PASS, all scenarios" "FAIL"
done

# ---- 4. LibreLane signoff metrics
F=$OUT/metrics.txt
header "$F" "LibreLane signoff metrics" librelane/snn_top/results/metrics.json
python3 - librelane/snn_top/results/metrics.json >> "$F" <<'EOF'
import json, sys
m = json.load(open(sys.argv[1]))
rows = [
    ("die area (um^2)", "design__die__area"),
    ("analog macro area (um^2)", "design__instance__area__macros"),
    ("standard cells, logic (count)", None),
    ("Magic DRC errors", "magic__drc_error__count"),
    ("KLayout DRC errors (all DCF.1a density)", "klayout__drc_error__count"),
    ("routing DRC errors", "route__drc_errors"),
    ("antenna violations (nets)", "antenna__violating__nets"),
    ("power grid violations", "design__power_grid_violation__count"),
    ("max slew / cap / fanout violations", None),
    ("setup violations (all corners)", "timing__setup_vio__count"),
    ("hold violations (all corners)", "timing__hold_vio__count"),
    ("worst setup slack (ns, 1000 ns clock)", "timing__setup__ws"),
    ("worst hold slack (ns)", "timing__hold__ws"),
    ("LibreLane LVS errors (macro black-boxed)", "design__lvs_error__count"),
]
logic = sum(m.get(f"design__instance__count__class:{c}", 0) for c in (
    "clock_buffer", "inverter", "multi_input_combinational_cell", "sequential_cell", "timing_repair_buffer"))
for label, key in rows:
    if key:
        val = m.get(key)
        val = f"{val:.2f}" if isinstance(val, float) else val
    elif label.startswith("standard"):
        val = logic
    else:
        val = "/".join(str(m.get(f"design__max_{k}_violation__count")) for k in ("slew", "cap", "fanout"))
    print(f"{label:45s} {val}")
print()
print("per corner: setup / hold worst slack (ns)")
for c in ("ss_125C_3v00", "tt_025C_3v30", "ff_n40C_3v60"):
    for r in ("min", "nom", "max"):
        k = f"{r}_{c}"
        print(f"  {k:20s} {m[f'timing__setup__ws__corner:{k}']:8.2f}  {m[f'timing__hold__ws__corner:{k}']:6.2f}")
EOF

# ---- 5. layout pictures
python3 signoff/make_layout_png.py > /dev/null

echo
{ echo "# signoff/run_checks.sh ${1:-}, $(date '+%F %H:%M'), commit $REV"
  printf '%s\n' "${STATUS[@]}"; } | tee "$OUT/STATUS.txt"
echo "results: signoff/results/, plots: signoff/img/"
! printf '%s\n' "${STATUS[@]}" | grep -q '^FAIL'
