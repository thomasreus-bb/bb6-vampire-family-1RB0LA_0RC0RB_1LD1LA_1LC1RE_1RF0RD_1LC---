# No. 83 (`1RB1RA_1LC0RB_1LD0LB_1RA0LE_---1LF_1LB0LA`): Bell map, exact orbit, HALT condition, coin model (27 Nov 2026)

Mirrored TM `1LB1LA_1RC0LB_1RD0RB_1LA0RE_---1RF_1RB0RA` (the rare records are on the left).
The scripts were run in `/tmp/an83/`; paths are hard-coded.

## Bell structure

A Bell starts at a left record in state B with the tape

    0 1^N 0^r S        (N odd and large, r ∈ {1, 3}; once r = 2)

1. **Sweep:** the head runs right through 1^N, turns it into 0^(N−1) and rewrites the front of S (about 5N steps).
2. **Slow phase:** A/B left records alternate; every pair eats 4 zeros and adds 6 ones on the left (about N² steps).
   S is not touched.
3. The next Bell has N' = 6·⌊(N−1)/4⌋ + 3 and r' = 1 if N ≡ 1 (mod 4), r' = 3 if N ≡ 3 (mod 4)
   (normal mode; in rarer modes the sweep also merges blocks of S, then N' = a·N + b with other a, b).

So N grows by a factor 3/2 per Bell (Collatz-like, N ≡ 3 mod 6), and r is a pseudo-random bit of N.
S is a list of 1-blocks separated by zero gaps. It grows by about 4.5 cells per Bell, and each Bell changes only
its first 10 to 100 cells: new blocks are pushed at the front, the old part stays.

## Tools

| file | purpose |
|---|---|
| `cyc83.c` | `cyc83 N r S maxsteps`: one full Bell from `0 1^N 0^r S` to the next Bell (or HALT) |
| `mac83.py`, `it83.py` | first version (sweep only, slow phase analytically); checked against the direct run |
| `orb83b.py` | exact orbit: each Bell with three representatives n ≡ N (mod 96), fit M = a·n + b, then M = a·N + b with big integers; writes `orb83.txt` (Bell, log10 N, N mod 96, r, S as run lengths) |
| `coin83.py`, `coin83log.py` | coin model: r random in {1, 3}, N replaced by a random small representative ≡ 3 (mod 6), S truncated to 600 cells |
| `front83.py`, `clos83.py` | tests of the HALT condition and of the front-block bound on synthetic S |

**Check:** the first 22 Bells of the direct simulation (to 4·10⁹ steps) agree exactly with the Bell map.

## Results

- **Exact orbit:** 1,079 Bells, N ≈ 10^190 at the end (the steps per Bell are of the order N², so the orbit
  covers far more than 10^300 TM steps). No HALT. S has 4,790 cells and 203 blocks at the end.
  All blocks have even length ≥ 6, the front block is always ≥ 6; r = 1 and r = 3 occur 538 times each, r = 2 once.
- **HALT condition** (grid: front block a ≤ 15, gap ≤ 12, next block 6 or 12, six values of N):
  the next Bell halts **exactly when the front block of S has length h(r)** with h(1) = 2, h(2) = 3, h(3) = 1,
  independent of the gap. Every non-halting Bell in this grid writes a new front block of length **≥ 5**.
  (For arbitrary S with short inner blocks other halts exist, but such S never occur in the orbit.)
- **Coin model:** 24 runs × 4,000 Bells plus 12 runs × 4,000 Bells = 144,000 random Bells: **0 HALT**.
  A front block shorter than 6 appeared in very few Bells (one logged case: front 5 after an odd gap 1), never the
  halting length h(r).

## Assessment

HALT needs a front block of length 1, 2 or 3 matched to r. The sweep always writes at least 5 ones at the front,
and S keeps blocks of length ≥ 6. So HALT is not a lottery here: the per-Bell chance is 0 in all observed and
sampled Bells. **Probably nonhalting.** A proof path: describe the reachable S language (blocks ≥ 6, even, gaps
≥ 2, with the rare odd cases) and show that the Bell map keeps it and never writes a front block ≤ 3.
