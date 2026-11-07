#!/usr/bin/env bash
# Download, compile and run the fast simulator for no. 35
# (1RB---_0RC0LD_1LB1RC_0LE0LF_1RD1LE_1RF1RA).
#
# usage:  bash run35.sh [EXP] [EVERY] [NEARMISS]
#   EXP       simulate up to 10^EXP steps            (default 19)
#   EVERY     print every EVERY-th left record        (default 100000)
#   NEARMISS  1 = also print every record with a small first or inner counter (default 0)
# examples:
#   bash run35.sh                 # 10^19 steps, a few seconds
#   bash run35.sh 22 1000000 1    # 10^22 steps with near misses, a few minutes
# needs: curl (or wget) and gcc on a 64-bit system (Linux, macOS, or WSL on Windows)
set -euo pipefail

EXP=${1:-19}
EVERY=${2:-100000}
NEAR=${3:-0}
URL="https://raw.githubusercontent.com/thomasreus-bb/bb6-vampire-family-1rb0la_0rc0rb_1ld1la_1lc1re_1rf0rd_1lc---/main/scan/m35/sim35.c"
DIR=${SIM35_DIR:-sim35}

mkdir -p "$DIR"
cd "$DIR"

echo "== download sim35.c"
if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$URL" -o sim35.c
elif command -v wget >/dev/null 2>&1; then
  wget -q "$URL" -O sim35.c
else
  echo "error: neither curl nor wget found" >&2; exit 1
fi

echo "== compile"
gcc -O2 -o sim35 sim35.c

OUT="run35_e${EXP}.txt"
echo "== run: up to 10^${EXP} steps, every ${EVERY}-th left record, near misses: ${NEAR}"
echo "   output also in $(pwd)/${OUT}"
if [ "$NEAR" = "1" ]; then
  NEARMISS=1 ./sim35 "$EXP" "$EVERY" | tee "$OUT"
else
  ./sim35 "$EXP" "$EVERY" | tee "$OUT"
fi
