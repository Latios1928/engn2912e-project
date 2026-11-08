#!/bin/bash
# Shell port of ngspice's `vlnggen` script: builds <top>.so for the d_cosim
# XSPICE model from Verilog, plus <top>_obj_dir/{inputs,outputs,inouts}.h,
# which list the ports in the order d_cosim expects them.
#
# Why not `ngspice -b vlnggen`: ngspice-46 lowercases the `shell` command
# line inside the script, so Verilator gets `--mdir`, `--cflags`, `--prefix
# vlng` and stops with "Invalid option: --mdir".
#
# Usage: vlnggen.sh [verilator options] top.v [more.v ...]
#   The .so is named after the first .v file and written to the current folder.
set -euo pipefail

NGSPICE_SRC=${NGSPICE_SRC:-/foss/tools/ngspice/share/ngspice/scripts/src}
VERILATOR=${VERILATOR:-/foss/tools/bin/verilator}
PREFIX=Vlng

base=""
for a in "$@"; do
  case "$a" in *.v) base=$(basename "$a" .v); break ;; esac
done
[ -n "$base" ] || { echo "vlnggen.sh: no .v file given" >&2; exit 1; }
objdir="${base}_obj_dir"

# 1. Verilog -> C++ (only to read the port list).
"$VERILATOR" --Mdir "$objdir" --prefix "$PREFIX" --CFLAGS -fpic --cc "$@"

# 2. Port headers, as vlnggen does:  VL_IN8(&clk,0,0); -> VL_DATA(8,clk,0,0)
#    (VL_INOUT is tested first because it also contains VL_IN.)
hdr="$objdir/$PREFIX.h"
# Ports over 64 bits (VL_INW/VL_OUTW) are skipped by vlnggen; the shim also
# reads bits with (1 << i), so keep every port at 31 bits or fewer.
if grep -qE 'VL_(IN|OUT|INOUT)W\(' "$hdr"; then
  echo "vlnggen.sh: wide ports are not supported by d_cosim (split them, max 31 bits):" >&2
  grep -E 'VL_(IN|OUT|INOUT)W\(' "$hdr" >&2
  exit 1
fi
for kind in inouts inputs outputs; do echo "/* Generated code: do not edit. */" >"$objdir/$kind.h"; done
sed -n -E 's/.*VL_INOUT([0-9]*)\(&([^)]*\)).*/VL_DATA(\1,\2/p' "$hdr" >>"$objdir/inouts.h"
grep -v 'VL_INOUT' "$hdr" | sed -n -E 's/.*VL_IN([0-9]*)\(&([^)]*\)).*/VL_DATA(\1,\2/p' >>"$objdir/inputs.h"
sed -n -E 's/.*VL_OUT([0-9]*)\(&([^)]*\)).*/VL_DATA(\1,\2/p' "$hdr" >>"$objdir/outputs.h"

# 3. Build with ngspice's shim and link a shared library.
"$VERILATOR" --Mdir "$objdir" --prefix "$PREFIX" --CFLAGS "-I$NGSPICE_SRC" --CFLAGS -fpic \
  --cc --build --exe "$NGSPICE_SRC/verilator_main.cpp" "$NGSPICE_SRC/verilator_shim.cpp" "$@"
g++ --shared "$objdir/verilator_shim.o" "$objdir/verilated.o" "$objdir/verilated_threads.o" \
  "$objdir/${PREFIX}__ALL.a" -pthread -lpthread -o "$base.so"
echo "vlnggen.sh: wrote $base.so"
