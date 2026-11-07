#!/usr/bin/env bash
# Download, compile and run the fast simulator for no. 16
# (1RB1LF_1RC1RF_0LD1RE_---1LC_0RB1RE_1LA0LE).
#
# usage:  bash run16.sh [EXP]
#   EXP   simulate up to 10^EXP steps (default 24; at most 36)
# examples:
#   bash run16.sh        # 10^24 steps, a few seconds
#   bash run16.sh 30     # 10^30 steps, about 7 minutes
# needs: curl (or wget) and gcc on a 64-bit system (Linux, macOS, or WSL on Windows)
set -euo pipefail

EXP=${1:-24}
URL="https://raw.githubusercontent.com/thomasreus-bb/bb6-vampire-family-1rb0la_0rc0rb_1ld1la_1lc1re_1rf0rd_1lc---/main/scan/m16/sim16.c"
DIR=${SIM16_DIR:-sim16}

mkdir -p "$DIR"
cd "$DIR"

echo "== download sim16.c"
if command -v curl >/dev/null 2>&1; then
  curl -fsSL "$URL" -o sim16.c
elif command -v wget >/dev/null 2>&1; then
  wget -q "$URL" -O sim16.c
else
  echo "error: neither curl nor wget found" >&2; exit 1
fi

echo "== compile"
gcc -O2 -o sim16 sim16.c

OUT="run16_e${EXP}.txt"
echo "== run: up to 10^${EXP} steps"
echo "   output also in $(pwd)/${OUT}"
nice ./sim16 "$EXP" | tee "$OUT"
