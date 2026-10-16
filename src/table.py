"""table.py - build the Bell transition table of a TM2-type machine by breadth-first search.

For every word P (starting with the empty word) and each parity of n, the machine is started
in 0^inf P (10)^n 11 Z> 0^inf for three values of n of that parity and run to the next Bell end
with the program cyc (see cyc.c). An entry is accepted only if all three runs give the same
successor P' and the same constant d in n' = (3n + d) / 2 (or all three halt).

Usage:  python3 table.py TM Z MAXWORDS OUT.json
        e.g. python3 table.py 1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC--- F 3000 TM2.json
Needs the compiled program cyc (cyc.exe on Windows) in the same directory.

Output (JSON): {"T": {P: {"0": [P', d] | ["HALT"], "1": ...}}, "bad": [...], "open": [...]}
with "0"/"1" = n mod 2, P = "e" for the empty word, "open" = words reached but not yet expanded.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CYC = os.path.join(HERE, "cyc.exe" if os.name == "nt" else "cyc")


def run(tm, Z, queries):
    """Run cyc in rule mode for a list of (P, n); return {(P, n): result}."""
    inp = "".join(f"{P} {n}\n" for P, n in queries)
    out = subprocess.run([CYC, "rule", tm, Z, "200000000"], input=inp,
                         capture_output=True, text=True).stdout.split("\n")
    res = {}
    for line in out:
        if not line:
            continue
        p = line.split()
        key = (p[0], int(p[1]))
        if p[3] == "HALT":
            res[key] = ("HALT",)
        elif p[3] in ("LIMIT", "OVF"):
            res[key] = (p[3],)
        else:
            res[key] = (p[3], int(p[4]))       # successor word, new n
    return res


def main():
    tm, Z, maxwords, outname = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    T, bad, seen, front = {}, [], {"e"}, ["e"]
    while front and len(T) < maxwords:
        def base(P):                            # smallest n used for word P
            return 2 * (0 if P == "e" else len(P)) + 12
        queries = [(P, base(P) + par + 2 * j) for P in front for par in (0, 1) for j in range(3)]
        res = run(tm, Z, queries)
        nxt = []
        for P in front:
            entry = {}
            for par in (0, 1):
                outs = []
                for j in range(3):
                    n = base(P) + par + 2 * j
                    o = res[(P, n)]
                    outs.append(o if len(o) == 1 else (o[0], 2 * o[1] - 3 * n))   # (P', d)
                parity = (base(P) + par) % 2
                if len(set(outs)) != 1:
                    bad.append((P, parity, outs))
                    entry[parity] = ("INCONSISTENT",)
                    continue
                entry[parity] = outs[0]
                if len(outs[0]) == 2 and outs[0][0] not in seen:
                    seen.add(outs[0][0])
                    nxt.append(outs[0][0])
            T[P] = entry
        front = nxt
    with open(outname, "w") as f:
        json.dump({"T": T, "bad": bad, "open": front}, f)
    halts = sum(1 for P in T for p in T[P] if T[P][p][0] == "HALT")
    print(f"{tm}: {len(T)} words, {len(front)} open, {len(bad)} inconsistent, {halts} HALT entries")


if __name__ == "__main__":
    main()
