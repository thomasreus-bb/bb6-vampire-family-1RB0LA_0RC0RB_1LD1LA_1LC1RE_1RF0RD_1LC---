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

## Towards a nonhalting proof: invariant language (27 Nov 2026, afternoon)

Idea: the coin model shows that the Collatz part (N, r) does not matter. So replace N by "N ≡ 3 (mod 6), large"
and let r ∈ {1, 3} be arbitrary. Then it is enough to find a language L of S words that the Bell map keeps and that
contains no halting front. Tests with `cyc83` on random words (`lang83*.py`, `exc83.py`):

| language tested | result |
|---|---|
| L2: blocks even ≥ 6, gaps even ≥ 2, r ∈ {1, 3} | 5,943 of 6,000 random words stay in L2. **All 57 escapes have first gap = 2** (r = 1: 49, r = 3: 8). No HALT. |
| L2 with r = 2 allowed | many escapes (r = 2 breaks the parity), as expected |
| blocks ≥ 6 of any parity, gaps ≥ 1 | 2,868 of 3,000 stay; 2 escapes (gap 1 before a 6-block → 5-block); 130 runs end in another mode (odd front block: the 1-run and S merge into one block that grows forever, nonhalting) |

**Excursions** (`exc83.py`, exact Bell steps with random 60-digit N ≡ 3 mod 6): from 600 random L2 words with first
gap 2 and r ∈ {1, 3}:
- 588 return to L2 within 1 to 13 Bells (via odd gaps and r = 2);
- 12 leave a buried odd pair (odd block followed by an odd gap, e.g. `1^25 0^9`, `1^37 0^5`) deeper in S, while
  the front goes on in the even mode for 30 Bells;
- **0 HALT, 0 other failures.**

**Status.** L2 is almost closed; the only leak is the gap-2 front, and its excursions end without HALT. A proof
needs a language L ⊇ L2 that also contains the excursion states and the buried odd pairs, and the finite list of
parametric Bell rules on the front of S (front block a, gap g, next blocks, each as linear rules with residues),
proved by induction like shift rules. This is a sizeable but finite case analysis; it has not been done yet.

## Rule catalogue for the front of S (27 Nov 2026, evening)

Measured with `cyc83` on parameter grids (`rules83.py`, `rules83g2.py`, `rules83odd.py`; raw output in `r1.txt`,
`r3.txt`, `g2.txt`, `odd.txt`). Notation: S = 1^a 0^g 1^b 0^h T, T = untouched rest; r = gap before S.
All results were the same for several N (903, 905, 1203) unless "r' from N" is noted; every output is linear
in the parameters. These are the candidate lemmas for induction proofs (each is a shift-rule statement).

**Main rules (g ≥ 4; tested a = 6…30, g = 4…20, b = 12):**

| r | condition | S' | r' |
|---|---|---|---|
| 1 | g = 4 | 1^(a+b+8) 0^h T | from N |
| 1 | g ≥ 6 | 1^(a+8) 0^(g−4) 1^b … | from N |
| 3 | g = 4 | 1^6 0^(a−2) 1^(b+6) 0^h T | from N |
| 3 | g ≥ 6 | 1^6 0^(a−2) 1^6 0^(g−4) 1^b … | from N |

**Gap 2 (tested a = 6…14, b = 6, 8, 12, h = 4…20):**

| r | condition | S' | r' |
|---|---|---|---|
| 1 | a ≡ 2 (mod 4) | 1^6 0^(h−4) T | fixed: 3 if b ≡ 2, 1 if b ≡ 0 (mod 4) |
| 1 | a ≡ 0 (mod 4) | 1^6 0^(b−3) 1^6 0^(h−4) T | 2 |
| 1 | a odd | 1^(a+5) 0^(b−1) 1^6 0^(h−4) T | from N |
| 3 | a even | 1^6 0^(h−4) T | fixed: 1 if b ≡ 2, 3 if b ≡ 0 (mod 4) |
| 3 | a odd | 1^6 0^(a−3) 1^6 0^(b−3) 1^6 0^(h−4) T | from N |

(h = 4 means that 0^(h−4) is empty and the new 1^6 merges with the next block of T.)

**r = 2 and odd gaps (tested a = 6, 8, 12, g = 1…13 odd, b = 6, 12):**

| r | condition | S' |
|---|---|---|
| 2 | g = 1 | 1^(b−1) … (a 5-block if b = 6) |
| 2 | g = 3 | 1^6 0^(b−4) 1^6 0^(h−4) … (merges into T) |
| 2 | g ≥ 5 | 1^6 0^(a−3) 1^6 0^(g−4) 1^b … |
| 1 | g = 5 | 1^(a+8) 0^1 1^b … |
| 1 | g ∈ {1, 3} | merges into T, r' = 2 |
| 3 | g = 1 | 1^(b−1) … |
| 3 | g = 5 | 1^6 0^(a−2) 1^6 0^1 1^b … |

**What this shows.**
1. In the even world L2 (r ∈ {1, 3}, blocks even ≥ 6, gaps even ≥ 4) the four main rules stay in L2 except that
   g = 6 produces a gap of 2. HALT is impossible there: the new front block is a + 8, a + b + 8 or 6.
2. Gap 2 is the only exit. With a ≡ 0 (mod 4) and r = 1 it starts the odd excursion (gap b − 3, r' = 2).
3. In the odd excursion the rules produce gaps 1, 3, 5 and, via gap 1, blocks b − 1 (e.g. 5). This is where the
   case list grows; the halting fronts (1, 2, 3) did not appear in any of these cases.

**Next steps for a proof.** Close the excursion: follow the r = 2 / odd-gap rules (including blocks of length 5
and b − 1, and the merges with T) until the word is back in L2, and check that every branch avoids the halting
fronts h(1) = 2, h(2) = 3, h(3) = 1. Then each table row becomes one inductive lemma (run lengths as parameters),
plus the two shift rules for the sweep and the slow phase.
