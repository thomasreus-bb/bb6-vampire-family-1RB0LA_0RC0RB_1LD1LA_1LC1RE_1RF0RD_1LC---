# No. 42: interim notes (13 Nov 2026, analysis in progress)

Machine `1RB0RF_1LC0RA_1LD1LB_0LE---_1LA0LA_1RE1LD`; the tape grows to the left. HALT: D reading 1.

Tools: `rec2.c` (prints the tape at every new leftmost cell), `comp.py` (writes it as (10)^a, 1^b, 0^z).

    gcc -O2 -o rec2 rec2.c
    ./rec2 1RB0RF_1LC0RA_1LD1LB_0LE---_1LA0LA_1RE1LD 300000000 100000 | python3 comp.py

Observed so far. C(a, b) means state A, head on the new left cell, tape `0 (10)^a 1^b R`:
- C(a, b) → C(a+2, b−2) for b ≥ 3 (the block 1^b is turned into (10) pairs, two cells per record).
- b = 1: C(a, 1) → C(1, 2a+6). Seen: a = 19 → 1^44, a = 78 → 1^162.
- b = 2: C(a, 2) → a long phase, then `0^3 (10)^c 1^d R` → C(1, 4) `0 (10)^c 1^d R`, i.e. a new segment on the left.
  Seen: a = 43 → c = 32, d = 31; a = 59 → c = 56, d = 15.
- Afterwards the two segments merge, e.g. C(3, 2) 0 (10)^32 1^31 → … → C(55, 6).

## Exact event rules (13 Nov 2026, checked in 8,120 cases with `ev42.c`, `rules42.py`)

Events: state A, head on a new leftmost cell. X(a,b) = tape (10)^a 1^b; Z(c,e) = tape 00 (10)^c 1^e.
- R1: X(a,b) → X(a+2, b−2) for b ≥ 3.
- R2: X(a,1) → X(1, 2a+6).
- R3: X(a,2): blocks D_k = 6·3^k − 1, A_k = 3^(k+1) − 3 − k (A = 0, 5, 22, 75, 236, …). For A_k ≤ a < A_(k+1), j = a − A_k:
  j = 0 → X(1, D_k); j = 2i+1 → Z(2+3i, D_k−2−2i); j = 2i+2 → X(4+3i, D_k−2−2i).
- Z(c,e) → X(1,4) 0 X(c,e) → X(3,2) 0 X(c,e) =: M(c,e) (two events).
- R4: M(c,e), c odd: e ≥ 2 → X(c+6, e−1); e = 1 → R3 result of X(c+4, 2).
- M(c,e), c even: no closed rule yet (several regimes). **M(c,2) with c even halts.**

Consequence: R1–R4 never produce Z(·,2) (D_k is odd). A HALT needs a merge M(c,e) with c even that produces Z(c'',2) with c'' even. Example: M(12,5) → Z(22,2) → HALT.

## Merges with even c (13 Nov 2026)

- For c even, M(c,e) halts **exactly for e in H**, independently of c (checked for c = 2, 4, 50, 52, 200, 1000 and e < 1500).
  H below 5000 (`hset_M2_e1-4999.txt`, from M(2,e)): 2, 28, 74, 114, 288, 622, 715, 772, 1044, 1209, 3391.
- Inside such a merge the block 1^e is erased and a new process grows from the right end into the gap until it meets the left part.
  The outcome depends on where this process stands when it meets the wall, so H is tied to the machine's own dynamics (as the Holdout Guide says).
- Since R1–R4 are exact and never halt, **the machine halts iff some merge M(c,e) with c even has e in H.**

## Macro orbit (`orbit42.py`)

Even merges of the real run (c, e): (32,31), (56,15), (266,307), (4214,1563), (5888,447), (6008,367), (314,39155), …; none has e in H.
