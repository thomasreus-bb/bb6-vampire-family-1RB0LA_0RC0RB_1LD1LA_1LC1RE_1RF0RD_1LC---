"""compare.py - the checks behind the family table in README.md.

1. Move sequences: which machine is which base machine started in which state (first 5,000 steps).
2. Tables: TM2a and TM2b against TM2 (parity swapped, d shifted by -1 / +1).
3. Orbits: the orbits of all machines in TM2 coordinates, iterated with the TM2 table;
   where they meet, and TM1's 23 directly simulated Bells reproduced.

Usage: python3 compare.py      (reads ../tables/TM2.json, TM2a.json, TM2b.json)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = os.path.join(HERE, "..", "tables")

MACHINES = {
    "TM1":   "1RB---_1LC0RB_0LD0LC_1RE1RB_1RD1LF_1LA0LE",
    "TM1-F": "1RB0RF_1LC---_1RD0LC_0RE0RD_1LF1LC_1LE1RA",
    "TM2":   "1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---",
    "TM2'":  "1RB0RE_1RC---_0RD0RC_1LE1LF_1LD1RA_1RC0LF",
    "TM2a":  "1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LA---",
    "TM2b":  "1RB---_0RC0RB_1LD1LE_1LC1RF_1RB0LE_1RA0RD",
    "TM2b'": "1RB0RF_1LC---_1LF1LD_1RE0LD_0RC0RE_1LC1RA",
}
BASE = "1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_"        # TM2 without state F
BASE_MACHINES = {"TM1": MACHINES["TM1"]}
for f0 in ("1LC", "1LA", "1RB"):
    BASE_MACHINES["TM2 with F0=" + f0] = BASE + f0 + "---"


def parse(tm):
    rules = {}
    for s, tr in enumerate(tm.split("_")):
        for b in (0, 1):
            p = tr[3 * b:3 * b + 3]
            rules[(s, b)] = None if p[0] == "-" else (int(p[0]), 1 if p[1] == "R" else -1, ord(p[2]) - 65)
    return rules


def moves(tm, start, n, mirror=False):
    """Sequence of (move, written symbol) of the first n steps from the blank tape."""
    rules, tape, h, st, out = parse(tm), {}, 0, start, []
    for _ in range(n):
        r = rules[(st, tape.get(h, 0))]
        if r is None:
            break
        tape[h] = r[0]
        mv = -r[1] if mirror else r[1]
        h += mv
        st = r[2]
        out.append((mv, r[0]))
    return out


def load(name):
    with open(os.path.join(TAB, name)) as f:
        return json.load(f)["T"]


def main():
    print("1. Move sequences (5,000 steps)")
    for name, tm in MACHINES.items():
        ref = moves(tm, 0, 5000)
        hits = [f"{bn} from {'ABCDEF'[s]}{' (mirrored)' if mir else ''}"
                for bn, b in BASE_MACHINES.items() for s in range(6) for mir in (False, True)
                if moves(b, s, 5000, mir) == ref]
        print(f"   {name:6s} = {', '.join(hits)}")

    T = load("TM2.json")
    print("2. Tables against TM2 (parity swapped)")
    for name in ("TM2a", "TM2b"):
        X, same, shifts, total = load(name + ".json"), 0, {}, 0
        for P in T:
            if P not in X:
                continue
            for p in "01":
                a, b = T[P]["1" if p == "0" else "0"], X[P][p]
                total += 1
                if a[0] == b[0]:
                    same += 1
                    if len(a) == 2:
                        shifts[b[1] - a[1]] = shifts.get(b[1] - a[1], 0) + 1
        print(f"   {name}: {same} of {total} entries with the same successor; d shifts {shifts}")

    print("3. Orbits in TM2 coordinates (n, P)")
    def orbit(n, P, N=3000):
        out = [(n, P)]
        for _ in range(N):
            o = T[P][str(n % 2)]
            if o[0] == "HALT":
                break
            n, P = (3 * n + o[1]) // 2, o[0]
            out.append((n, P))
        return out
    starts = {"TM1": (1, "e"), "TM1-F": (1, "1"), "TM2": (3, "e"), "TM2'": (4, "1"),
              "TM2a": (2, "e"), "TM2b": (4, "e"), "TM2b'": (4, "e")}
    orbits = {k: orbit(*v) for k, v in starts.items()}
    for k, o in orbits.items():
        print(f"   {k:6s}", " ".join(f"{n},{P}" for n, P in o[:8]))
    keys = list(orbits)
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            first = {x: a for a, x in enumerate(orbits[keys[i]])}
            meet = next(((first[x], b) for b, x in enumerate(orbits[keys[j]]) if x in first), None)
            if meet:
                print(f"   {keys[i]} and {keys[j]} meet (Bell {meet[0] + 1} / Bell {meet[1] + 1})")
    tm1_k = [2, 14, 32, 56, 92, 146, 224, 344, 524, 794, 1202, 1814, 2732, 4106, 6164, 9254, 13886,
             20840, 31268, 46910, 70373, 105566, 158354]
    ok = [n for n, P in orbits["TM1"][:23]] == [k // 2 for k in tm1_k]
    print(f"   TM1: the 23 directly simulated Bells (k) agree with n = floor(k/2): {ok}")


if __name__ == "__main__":
    main()
