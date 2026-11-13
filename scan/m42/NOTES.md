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

Open: the exact rule for b = 2 and the merge, then the counter system and where HALT can occur.
