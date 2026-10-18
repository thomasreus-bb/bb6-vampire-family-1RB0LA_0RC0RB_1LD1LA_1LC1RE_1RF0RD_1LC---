# A family of seven vampire-like BB(6) holdouts

Author: Thomas Reus, with the AI model Claude Opus 5.5  
Status: 18 Oct 2026 (draft; labels such as TM2a or TM2' are provisional)

This repository is about a **family of seven "energy vampire"-like Turing machines** from the recent holdout list (BB6_holdouts_663).

All seven machines turn out to be **one machine core with three variants of a single transition, started in different states**. They iterate the same map, but on four different orbits.

**Terminology: Bell = cycle.** The run of each machine splits into *Bells*. The TM1 notes call them Bells, the TM2 notes and the Discord thread call them cycles; both words mean the same. This document uses **Bell** throughout.

The first machine of this investigation, TM1, has its own repository with the fast simulation to 10⁹ Bells:
[bb6-1RB---_1LC0RB_0LD0LC_1RE1RB_1RD1LF_1LA0LE](https://github.com/thomasreus-bb/bb6-1RB---_1LC0RB_0LD0LC_1RE1RB_1RD1LF_1LA0LE).
Data of TM1 are not copied here; this document refers to that repository.

## Simulation status (18 Oct 2026, 16:38 CEST)
- **Orbit O1** (TM1): simulated to **Bell 2·10⁹ without a halt** with [`orbits/O1`](orbits/O1) (KCHECK `15888523420693262708 1169925006 10001`; k has 1,169,925,006 bits).
- **Double-check:** an independent run on a second computer reproduces the KCHECK values at Bells 6·10⁸, 7·10⁸, 8·10⁸, 9·10⁸ and 10⁹ (`8610941070033361538 584962505 1101`); continued to Bell 1,000,000,005 it gives `825729492582408624 584962508 10001`, the reference value of the TM1 repository.
- **Planned:** all four orbits up to Bell 10¹⁰ (O1 first) on my notebook with 16 GB RAM; later 10¹¹ with external help (about 64 GB RAM required).
- **Halting probability** (Markov estimate, see [below](#halt-expected-markov-estimate)): up to Bell 10¹⁰ about 0.9 % per orbit (3.5 % for at least one of the four orbits), up to Bell 10¹¹ about 8.5 % per orbit (30 % for at least one); the value for four orbits assumes that they behave like independent random sequences.

## In brief
All seven machines iterate, as far as we can see, the same map on pairs (n, P):

    n' = (3n + d) / 2 ,      (P', d) = f(P, n mod 2)          (TM2 coordinates, see below)

or HALT. They differ only in how the end of a Bell is encoded on the tape (a shift of n by ±1, a swapped parity, or a mirror image) and in where they start.
The seven machines run on **four different orbits** O1 to O4. A halt on one orbit says nothing about the others.

| Label | Machine | Core + F0, start state | Orbit | DeepMind paper (15 Oct 2026) |
|---|---|---|---|---|
| TM1 | `1RB---_1LC0RB_0LD0LC_1RE1RB_1RD1LF_1LA0LE` | F0 = `1LA`, start F, mirrored | **O1** | — |
| TM1-F | `1RB0RF_1LC---_1RD0LC_0RE0RD_1LF1LC_1LE1RA` | F0 = `1LA`, start E | **O2** | candidate list (App. C) |
| TM2 | `1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---` | F0 = `1LC`, start A | **O2** | candidate list (App. C) |
| TM2' | `1RB0RE_1RC---_0RD0RC_1LE1LF_1LD1RA_1RC0LF` | F0 = `1RB`, start E | **O2** | — |
| TM2a | `1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LA---` | F0 = `1LA`, start A | **O3** | — |
| TM2b | `1RB---_0RC0RB_1LD1LE_1LC1RF_1RB0LE_1RA0RD` | F0 = `1RB`, start A (or F, same run) | **O4** | — |
| TM2b' | `1RB0RF_1LC---_1LF1LD_1RE0LD_0RC0RE_1LC1RA` | F0 = `1LC`, start E | **O4** | — |

## The machine core
All seven machines are, after renaming the states (Tree Normal Form) and possibly mirroring the tape, the machine

    A  1RB0LA
    B  0RC0RB
    C  1LD1LA
    D  1LC1RE
    E  1RF0RD
    F  ???---          F0 = 1LC (TM2), 1LA (TM2a) or 1RB (TM2b)

started on the blank tape in state A, E or F. "F0" is the transition of state F reading 0. It is executed exactly once per Bell, at the end of the Bell, so changing it changes only the hand-over to the next Bell, not the Bell itself.
This was checked by comparing the sequences of moves and written symbols for the first 5,000 steps (`src/compare.py`). In particular, **TM1 is the mirror image of TM2 with F0 = `1LA`, started in state F.**

Started in A, E or F, the three variants give 9 runs; the seven machines of the list are among them:

| | start A | start E | start F |
|---|---|---|---|
| F0 = `1LC` | TM2 | TM2b' | — (not in the list) |
| F0 = `1LA` | TM2a | TM1-F | TM1 (mirrored) |
| F0 = `1RB` | TM2b | TM2' | TM2b |

## The common dynamics (TM2 coordinates)
We use TM2 as the reference. A Bell of TM2 ends in the configuration

    0^∞  P  (10)^n  11  F>  0^∞        (n maximal; P is a short word, empty or starting with 1)

and the next Bell ends with n' = (3n + d)/2 and the word P', where (P', d) depends only on P and on n mod 2, or in HALT.
(TM1 is described in its own repository by the *start* of a Bell, `0^∞ 1^k F> S 0^∞`; that is a different point of the same Bell.)

- **Table.** For TM2 the table built by breadth-first search holds 49,993 words, 810 of them HALT entries ([TM2.md](TM2.md)). The two HALT words that carry almost all of the halt rate are `1111` and `111101`, each for n odd.
- **Markov estimate** (fair-coin assumption, not proved): halt rate 8.87·10⁻¹³ per Bell; see "HALT expected!" below.
- **Shortest halting path** (computed for TM1, so it holds for the common graph): 41 transitions from the word ε with n even.
- **Memory demand and step count:** n grows by about 3/2 per Bell, i.e. 0.585 bits per Bell; one Bell takes about (3/2)·n² TM steps (TM2 coordinates); see "Fast simulation" below.

**How the tables were compared.** For TM2, TM2a and TM2b we built tables of about 3,000 words each with the same program (`src/cyc.c`, `src/table.py`; three values of n per entry, no inconsistencies). The TM2 table reproduces the excerpt in [TM2.md](TM2.md).
For TM1 the comparison with TM2 was made earlier ([TM2.md](TM2.md), "Relation to TM1"). For TM1-F, TM2' and TM2b' no own table was built; they are identified through the machine core and their orbits.

| Machine | conversion to TM2 coordinates | entries compared | agree |
|---|---|---|---|
| TM1 | n = ⌊k/2⌋, P = (S without leading `11`) read backwards | 91,130 | 83,324 directly, the rest differ only in the encoding of the Bell boundary |
| TM2a | n<sub>TM2</sub> = n − 1 (parity swapped, d − 1) | 5,994 | 5,984, all 44 HALT entries included; the other 10 differ by one `10` pair at the boundary |
| TM2b | n<sub>TM2</sub> = n + 1 (parity swapped, d + 1) | 5,994 | 5,984, same as TM2a |

Check of the conversion: iterating the TM2 table from TM1's first Bell (n = 1, P = ε) reproduces k/2 for all 23 directly simulated Bells of TM1 (up to k = 158,354).

## The four orbits
All in TM2 coordinates (n, P), ε = empty word. Each orbit was iterated for 3,000 Bells with the TM2 table: O1 to O4 never meet; TM1-F joins the orbit of TM2 at its Bell 4 (= TM2's Bell 3), TM2' at its Bell 2.

| Bell | O1: TM1 | O2: TM2 (TM1-F, TM2') | O3: TM2a | O4: TM2b (TM2b') |
|---:|---|---|---|---|
| 1 | 1, ε | 3, ε | 2, ε | 4, ε |
| 2 | 7, ε | 10, ε | 7, `1` | 10, `1` |
| 3 | 16, ε | 19, `1` | 13, `1000` | 19, ε |
| 4 | 28, `1` | 31, `1000` | 25, `1` | 34, ε |
| 5 | 46, ε | 52, `1` | 40, `1000` | 55, `1` |
| 6 | 73, `1` | 82, ε | 64, `101` | 85, `1000` |
| 7 | 112, `1000` | 127, `1` | 100, `1` | 133, `1` |
| 8 | 172, `101` | 193, `1000` | 154, ε | 202, `1000` |
| 9 | 262, `1` | 295, `1` | 235, `1` | 307, `101` |

## HALT expected! (Markov estimate)
This is a heuristic, not a proof. It is taken over from the TM1 and TM2 notes, where it was computed independently with the same result.

**Reasoning.** The next word P' and the question whether the machine halts depend only on P and on the parity of n (bit 1 of k in TM1). If this parity behaves like a fair coin in every Bell, the sequence of words is a Markov chain on the table, and every HALT entry ends the chain.
The visit frequencies of the chain agree with the real orbits (TM1: total variation distance 0.003 over 300,000 Bells; TM2: 0.0013 over 10⁶ Bells).

- **Halt rate:** 8.87·10⁻¹³ per Bell, almost all of it (61 % and 39 %) through the HALT words `1111` and `111101` (TM2 coordinates).
- **Expected** (per orbit): 1.13·10¹² Bells until the halt, median 7.8·10¹¹.

| Bells N | P(halt up to N) per orbit |
|---|---|
| 10⁹ | 0.089 % |
| 10¹⁰ | 0.88 % |
| 10¹¹ | 8.5 % |
| 10¹² | 58.8 % |
| 2·10¹² | 83 % |
| 5·10¹² | 98.8 % |

The model has no memory: if there is still no halt after N Bells, the chances for the next N Bells are the same again.

**Limits.** The fair-coin assumption is not proven: the parities come from the 3/2 dynamics, so correlations are possible, and they could change all the numbers above (even whether a halt ever happens).
So far only O1 (TM1, 10⁹ Bells) and O2 (TM2, 10⁶ Bells) have been simulated far enough to say anything; at the probabilities above, these runs could not have shown a halt anyway.

## Fast simulation
For TM1 there is a fast simulation, `bellntt` in the TM1 repository. It does not simulate the tape but the map on (k, S) with the table, and it is written so that very long numbers stay cheap:

- **Block simulation.** Each Bell uses up one bit from the bottom of k, so a block of B Bells depends only on the lowest B + 2 bits of k. Write k = q·2<sup>B+2</sup> + r; after B Bells the new k is 3<sup>B</sup>·q·4 + L, where L is computed from the short number r alone with the table.
- **Fast multiplication.** The long part q is multiplied once per block by 3<sup>B</sup>, with an own number theoretic transform (NTT: two 63-bit primes, Chinese remainder theorem, Montgomery arithmetic, OpenMP, no GMP).
- **Check.** At the end the program prints a fingerprint `KCHECK <k mod 2⁶⁴> <bit length> <S>`; two programs with the same fingerprint have computed the same orbit.

Run times and memory (TM1, 2 cores; times beyond 10⁹ Bells extrapolated with N^1.5, accurate to about a factor 3). The memory is that of the number k (about 0.585 bits per Bell) without the working buffers of the multiplication (observed at 8·10⁸ Bells: about 220 MB in total). The TM steps are a lower bound, from one Bell taking at least 3/8·k² steps:

| Bells N | run time `bellntt` | bits of k | memory for k | TM steps, lower bound |
|---|---|---|---|---|
| 10⁹ | 23 min (measured, no halt) | 585 million | 73 MB | 10<sup>3.52·10⁸</sup> |
| 10¹⁰ | ≈ 12 h | 5.85 billion | 0.73 GB | 10<sup>3.52·10⁹</sup> |
| 10¹¹ | ≈ 16 days | 58.5 billion | 7.3 GB | 10<sup>3.52·10¹⁰</sup> |
| 10¹² | ≈ 1.4 years | 585 billion | 73 GB | 10<sup>3.52·10¹¹</sup> |

For comparison, the simple reference program `bellrun` (40 Bells per pass over k, time ∝ N²) needs 12 s for 10⁷ Bells, 27 min for 10⁸ and about 2 days for 10⁹.

**For the family.** The same method works for every orbit of the family, since they all have the same map. The directories `orbits/O1` … `orbits/O4` each contain `bellntt` for one orbit, with the TM1 table, a start checkpoint and a reference checkpoint; the program writes text checkpoints, continues from the last one and stops at a given target Bell (see `orbits/O2/README.md`). All four orbits to 10¹² Bells would take about 4 × 1.4 years on 2 cores, or correspondingly less on more cores.

---

## TM1

    1RB---
    1LC0RB
    0LD0LC
    1RE1RB
    1RD1LF
    1LA0LE

- **Core:** F0 = `1LA`, started in F, tape mirrored (block of ones on the left, growing `(01)^m` part on the right; in TM2 the other way round).
- **Bell configuration (own form, start of a Bell):** `0^∞ 1^k F> S 0^∞`, next Bell k' = 3·⌊k/2⌋ + c, (S', c) = f(S, bit 1 of k).
- **Conversion:** n = ⌊k/2⌋, P = S without the leading `11`, read backwards (e.g. `110001` ↔ `1000`). HALT words `111111` ↔ `1111`, `11101111` ↔ `111101`.
- **Orbit:** O1 (own orbit).
- **First Bells** (direct simulation; t = steps before the Bell starts):

| Bell | t | k | S | TM2 coord. (n, P) |
|---:|---:|---:|---|---|
| 1 | 8 | 2 | `11` | 1, ε |
| 2 | 105 | 14 | `11` | 7, ε |
| 3 | 430 | 32 | `11` | 16, ε |
| 4 | 1,237 | 56 | `111` | 28, `1` |
| 5 | 2,930 | 92 | `11` | 46, ε |
| 6 | 7,217 | 146 | `111` | 73, `1` |
| 7 | 16,716 | 224 | `110001` | 112, `1000` |
| 8 | 38,163 | 344 | `11101` | 172, `101` |

- **Status:** simulated to 10⁹ Bells without a halt (`bellntt`), own table with 2,880 words; see the TM1 repository.

## TM1-F

    1RB0RF
    1LC---
    1RD0LC
    0RE0RD
    1LF1LC
    1LE1RA

- **Core:** F0 = `1LA`, started in E. Equivalently: TM1 started in state F instead of A (renamed, mirrored).
- **Bell configuration:** seen from TM1 as above. In its own naming the machine has a TM2-type Bell end, `0^∞ P (10)^n 11 B> 0^∞`, with n = n<sub>TM2</sub> + 1.
- **Orbit:** O2, **the same orbit as TM2** from TM1-F's Bell 4 / TM2's Bell 3 on.
- **First Bells** (TM1 started in F, direct simulation, TM1 form):

| Bell | t | k | S | TM2 coord. (n, P) |
|---:|---:|---:|---|---|
| 1 | 13 | 2 | `111` | 1, `1` |
| 2 | 80 | 8 | `110001` | 4, `1000` |
| 3 | 251 | 20 | `11101` | 10, `101` |
| 4 | 616 | 38 | `111` | 19, `1` (= TM2 Bell 3) |
| 5 | 1,583 | 62 | `110001` | 31, `1000` |
| 6 | 3,900 | 104 | `111` | 52, `1` |
| 7 | 8,881 | 164 | `11` | 82, ε |
| 8 | 20,908 | 254 | `111` | 127, `1` |

- **Status:** no own runs beyond 2·10⁷ steps; its orbit is covered by the runs for TM2.

## TM2

    1RB0LA
    0RC0RB
    1LD1LA
    1LC1RE
    1RF0RD
    1LC---

- **Core:** F0 = `1LC`, started in A. The reference machine of this document.
- **Bell end:** `0^∞ P (10)^n 11 F> 0^∞`, F reads 0 and goes on with F0 = `1LC`.
- **Orbit:** O2 (shared with TM1-F and TM2').
- **First Bells** (direct simulation; t = steps up to the end of the Bell):

| Bell | t | n | P |
|---:|---:|---:|---|
| 1 | 27 | 3 | ε |
| 2 | 178 | 10 | ε |
| 3 | 595 | 19 | `1` |
| 4 | 1,534 | 31 | `1000` |
| 5 | 3,813 | 52 | `1` |
| 6 | 8,738 | 82 | ε |
| 7 | 20,675 | 127 | `1` |
| 8 | 47,318 | 193 | `1000` |

- **Status:** direct simulation to Bell 24 (2·10¹⁰ steps), macro simulation to 10⁶ Bells, no halt ([TM2.md](TM2.md)). Discord thread with earlier work; listed as a candidate in the DeepMind paper.

## TM2'

    1RB0RE
    1RC---
    0RD0RC
    1LE1LF
    1LD1RA
    1RC0LF

- **Core:** F0 = `1RB`, started in E (renamed). The same variant started in A is TM2b.
- **Bell end (own naming):** `0^∞ P (10)^n 11 B> 0^∞`, with n = n<sub>TM2</sub> − 1.
- **Orbit:** O2, **the same orbit as TM2** from Bell 2 on.
- **First Bells** (direct simulation):

| Bell | t | n | P | TM2 coord. |
|---:|---:|---:|---|---|
| 1 | 32 | 3 | `1` | 4, `1` |
| 2 | 137 | 9 | ε | 10, ε (= TM2 Bell 2) |
| 3 | 518 | 18 | `1` | 19, `1` |
| 4 | 1,405 | 30 | `1000` | 31, `1000` |
| 5 | 3,604 | 51 | `1` | 52, `1` |
| 6 | 8,413 | 81 | ε | 82, ε |

- **Status:** Bell lengths identical to TM2 over 3·10⁸ steps (16 Bells, `scan/bellscan.c`).

## TM2a

    1RB0LA
    0RC0RB
    1LD1LA
    1LC1RE
    1RF0RD
    1LA---

- **Core:** F0 = `1LA`, started in A; otherwise identical to TM2. The same variant started in F is TM1 (mirrored), started in E it is TM1-F.
- **Bell end:** `0^∞ P (10)^n 11 F> 0^∞`, with n = n<sub>TM2</sub> + 1; parity swapped relative to TM2, d smaller by 1. HALT words therefore with n even: `1111`, `111101`.
- **Orbit:** O3 (own orbit).
- **First Bells** (direct simulation):

| Bell | t | n | P | TM2 coord. |
|---:|---:|---:|---|---|
| 1 | 27 | 3 | ε | 2, ε |
| 2 | 144 | 8 | `1` | 7, `1` |
| 3 | 415 | 14 | `1000` | 13, `1000` |
| 4 | 1,100 | 26 | `1` | 25, `1` |
| 5 | 2,613 | 41 | `1000` | 40, `1000` |
| 6 | 6,036 | 65 | `101` | 64, `101` |
| 7 | 13,385 | 101 | `1` | 100, `1` |
| 8 | 30,234 | 155 | ε | 154, ε |

- **Status:** own table (3,001 words, 44 HALT entries, `tables/TM2a.json`); macro simulation to 10⁵ Bells without halt; reproduces the first 14 directly simulated Bells.

## TM2b

    1RB---
    0RC0RB
    1LD1LE
    1LC1RF
    1RB0LE
    1RA0RD

- **Core:** F0 = `1RB`, started in A or F (both give the same run); renamed (TM2's A, E, F are called E, F, A here). The same variant started in E is TM2'.
- **Bell end (own naming):** `0^∞ P (10)^n 11 A> 0^∞`, with n = n<sub>TM2</sub> − 1; parity swapped relative to TM2, d larger by 1.
- **Orbit:** O4 (shared with TM2b').
- **First Bells** (direct simulation):

| Bell | t | n | P | TM2 coord. |
|---:|---:|---:|---|---|
| 1 | 27 | 3 | ε | 4, ε |
| 2 | 162 | 9 | `1` | 10, `1` |
| 3 | 477 | 18 | ε | 19, ε |
| 4 | 1,500 | 33 | ε | 34, ε |
| 5 | 3,945 | 54 | `1` | 55, `1` |
| 6 | 9,440 | 84 | `1000` | 85, `1000` |
| 7 | 22,277 | 132 | `1` | 133, `1` |
| 8 | 51,094 | 201 | `1000` | 202, `1000` |

- **Status:** own table (3,003 words, 45 HALT entries, `tables/TM2b.json`); macro simulation to 10⁵ Bells without halt; reproduces the first 14 directly simulated Bells.

## TM2b'

    1RB0RF
    1LC---
    1LF1LD
    1RE0LD
    0RC0RE
    1LC1RA

- **Core:** F0 = `1LC`, started in E; that is, TM2 itself started in E instead of A (renamed).
- **Bell end (own naming):** `0^∞ P (10)^n 11 B> 0^∞`, n in TM2 coordinates.
- **Orbit:** O4, **the same orbit as TM2b** from Bell 1 on.
- **First Bells** (direct simulation):

| Bell | t | n | P |
|---:|---:|---:|---|
| 1 | 40 | 4 | ε |
| 2 | 199 | 10 | `1` |
| 3 | 546 | 19 | ε |
| 4 | 1,625 | 34 | ε |
| 5 | 4,154 | 55 | `1` |
| 6 | 9,773 | 85 | `1000` |

- **Status:** Bell lengths identical to TM2b over 3·10⁸ steps (16 Bells, `scan/bellscan.c`).

---

## How the family was found
A quick scan of the 663 BB(6) holdouts (`scan/holdouts_663.txt`) for Bell behaviour (`scan/bellscan.c`, 10⁷ steps per machine) found 56 machines with Bell-like growth (`scan/bell_candidates.txt`).
Seven of them (class A) grow very regularly by a factor of about 1.56 per Bell; these are the seven machines above. The other 49 grow with other factors or less regularly and have not been analysed.

## Open points
- The identifications are observations from simulations and tables (checked for finitely many cases), not proofs.
- Markov estimate for the orbits O3 and O4 not recomputed (expected: the same as for TM1/TM2).
- Simulations far beyond 10⁵ Bells exist only for O1 (TM1, 10⁹ Bells) and O2 (TM2, 10⁶ Bells).
- Long runs of the fast simulation (`orbits/`) for O2, O3 and O4 are still to be done.
- **From a HALT to a Coq proof.** If an orbit reaches a HALT entry, a formal proof would consist of (1) the Turing machine semantics (available from the bbchallenge Coq work), (2) the few steps from the blank tape to the first Bell, (3) one lemma per table entry, `0^∞ 1^k F> S 0^∞` → `0^∞ 1^(3⌊k/2⌋+c) F> S' 0^∞` for all k by induction (several thousand lemmas, but uniform, so the proof scripts can be generated from the table), (4) the reduction "the machine halts iff the iterated Bell map reaches HALT", and (5) the computation of the orbit up to the halting Bell. Parts (1)–(4) look feasible; part (5) is the open problem: about 10¹² iterations with numbers of up to ~10¹¹ bits are far beyond what Coq can compute itself, and the orbit is pseudo-random, so there is no closed formula to shortcut it. A realistic route would be a Coq proof of (1)–(4) together with the computation done outside Coq by at least two independently written programs on different computers, agreeing in their checkpoint values (KCHECK); whether bbchallenge accepts such a combined proof is to be asked. A halt after roughly 10^(10¹¹) steps would not be a new BB(6) record, but it would decide every machine of the family on the halting orbit.

## Files
| Path | Content |
|---|---|
| `orbits/O1` … `orbits/O4` | fast simulation (`bellntt`) of one orbit each, with table and checkpoints; each directory can be copied and used on its own |
| `TM2.md` | detailed notes on TM2 (table, Markov estimate, Discord history) |
| `src/cyc.c` | Bell simulator for the TM2-type machines: direct simulation, and single Bells from a given (P, n) |
| `src/table.py` | builds a table by breadth-first search with `cyc` |
| `src/compare.py` | the checks behind this document: machine core, tables against TM2, orbits |
| `tables/TM2.json`, `TM2a.json`, `TM2b.json` | tables of TM2, TM2a, TM2b (about 3,000 words each) |
| `scan/bellscan.c`, `scan/bell_candidates.txt`, `scan/holdouts_663.txt` | Bell detector, its results, and the list of holdouts it was run on |

## Usage
**Long simulations** (fast, with checkpoints): see `orbits/O1` … `orbits/O4`, for example

    cd orbits/O2
    gcc -O3 -march=native -fopenmp -o bellntt bellntt.c -lm
    ./bellntt                                # continue from the newest checkpoint until HALT or Ctrl-C

**Checks and tables** (the programs in `src/` simulate the tape step by step; they are slow and meant for checks of the first Bells, not for long runs):

    cd src
    gcc -O2 -o cyc cyc.c
    ./cyc real 1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC--- F 10          # first 10 Bell ends of TM2
    python3 table.py 1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC--- F 3000 TM2.json
    python3 compare.py

    cd ../scan
    gcc -O2 -o bellscan bellscan.c -lm
    ./bellscan 1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC--- 10000000 300000000

An independent review of this investigation would be desirable.

## License
MIT
