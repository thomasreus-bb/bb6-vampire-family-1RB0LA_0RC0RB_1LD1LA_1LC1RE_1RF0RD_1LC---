#!/bin/bash
# try.sh TM "CERT" TIMEOUT : prints TM | CERT | true/false/timeout
export PATH=/opt/coq/bin:$PATH
TM=$1; CERT=$2; TO=$3
f=$(mktemp -p /home/claude/ctltry t_XXXXXX.v)
cat > $f <<EOV
From BusyCoq Require Import CTL62.
Eval vm_compute in (decide_nonhalt (TM_from_str "$TM") ($CERT)).
EOV
r=$(timeout $TO coqc -Q /home/claude/ccz181078/busycoq/verify BusyCoq -Q /home/claude/ccz181078/busycoq/verify/BigInt BigInt $f 2>&1 | grep -o "true\|false" | head -1)
[ -z "$r" ] && r=timeout
echo "$TM | $CERT | $r"
rm -f $f ${f%.v}.vo ${f%.v}.vok ${f%.v}.vos ${f%.v}.glob $(dirname $f)/.$(basename ${f%.v}).aux
