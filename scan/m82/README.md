# No. 82 (`1RB0RE_0LC1LE_0RD1LD_1RA1LF_1LC0RA_0LB---`): exact event orbit (27 Nov 2026)

Mirrored TM `1LB0LE_0RC1RE_0LD1RD_1LA1RF_1RC0LA_0RB---`; events = left records in state E.
Tools: `scan/orbit_tools/` (`orbit.py`, `learn.py`, `evstep.py`, `synthev.c`). `run82.py` writes `orb82.txt`
(one line per event: event number, W, log10 n, S).

**Event form.** The tape at an event is `W 0^n S` with W ∈ {`0001`, empty} (alternating) and

    S = (100)^k 1101 11 0^z 1101

**Two-counter cycle** (from `orb82.txt`): k counts up while z counts down. When z reaches 0, the blocks merge,
k is reset to 0 and a new zero run is written with z' = 3·z_max + 4 (observed: 34 → 106 → 322). The cycles grow
geometrically; between two resets the form of S is the same.

**Exact orbit:** 1,500 events, n ≈ 10^137 at the end (the Holdout Guide simulated to 2.7·10^79 steps).
No HALT. The 710 learned rules along the orbit (moduli 1 and 4) contain **no HALT entry in any residue class**.

**Coin model not valid here.** The residues of n are structurally constrained along the orbit (fixed residues at
the E events). With random residues the coin model produced messy S words and spurious halts (1.7 % per step);
those states are not reachable.

**Assessment.** Deterministic counter structure, not a lottery. **Probably nonhalting.** A proof would need the
cycle rule (k, z) → (0, 3z + 4) as an inductive statement for all z, together with the residue invariant of n.
