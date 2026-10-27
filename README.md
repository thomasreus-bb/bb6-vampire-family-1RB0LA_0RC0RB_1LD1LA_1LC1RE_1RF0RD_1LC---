# A family of seven vampire-like BB(6) holdouts

Author: Thomas Reus, with the AI model Claude Opus 5.5  
Status: 22 Oct 2026 (draft; labels such as TM2a or TM2' are provisional)

This repository is about a **family of seven "energy vampire"-like Turing machines** from the recent holdout list (BB6_holdouts_663).

All seven machines turn out to be **one machine core with three variants of a single transition, started in different states**. They iterate the same map, but on four different orbits.

**Terminology: Bell = cycle.** The run of each machine splits into *Bells*. The TM1 notes call them Bells, the TM2 notes and the Discord thread call them cycles; both words mean the same. This document uses **Bell** throughout.

The first machine of this investigation, TM1, has its own repository with the fast simulation to 10⁹ Bells:
[bb6-1RB---_1LC0RB_0LD0LC_1RE1RB_1RD1LF_1LA0LE](https://github.com/thomasreus-bb/bb6-1RB---_1LC0RB_0LD0LC_1RE1RB_1RD1LF_1LA0LE).
Data of TM1 are not copied here; this document refers to that repository.

> **The method works: first HALT found (21 Oct 2026).** The same approach (Bell structure → finite table for the Bell map → Markov estimate → fast exact simulation) applied to another BB(6) holdout from the scan, `1RB0RB_1LC1RF_0RD0LB_0RA1LE_1LD---_0RB0RC` ("vampire-like in base 3": n' = (4n + c)/3, 192 words, halting rate ≈ 1.6·10⁻⁹ per Bell), found a **HALT at Bell 298,793,335**, checked against the real Turing machine. See [Halt-found-1RB0RB_1LC1RF_0RD0LB_0RA1LE_1LD---_0RB0RC](https://github.com/thomasreus-bb/Halt-found-1RB0RB_1LC1RF_0RD0LB_0RA1LE_1LD---_0RB0RC).

## Simulation status (27 Oct 2026)
No halt has been found on any of the four orbits.

| orbit | machines | reached without halt | confirmed independently | closest approach (D) |
|---|---|---|---|---|
| O1 | TM1 | **10¹¹** (Ersen) | **at 10¹⁰** (`bellntt` = Ersen); Ersen's two engines agree up to 4.3·10¹⁰ | – |
| O2 | TM2, TM1-F, TM2' | **4.2·10¹¹** (Thomas Reus, `belldc` / `belldco`, run towards 10¹² in progress; Ersen 10¹¹) | **up to 10¹¹** (two programs); 10¹¹ … 1.4·10¹¹ two runs | **3** (Bell 139,153,319,148) |
| O3 | TM2a | **1.7·10¹¹** (Duke, `belldcf`, run towards 10¹² in progress; Ersen 10¹¹) | up to 10¹¹ (Duke = Ersen); up to 1.4·10¹⁰ also Andrew Ducharme, at 10¹⁰ also `belldc` | **3** (Bell 112,674,809,806) |
| O4 | TM2b, TM2b' | **2.25·10¹¹** (Andrew Ducharme, `belldc`; last KCHECK at 1.75·10¹¹) | at 10¹⁰ (`belldc`) | **5** (Bell 126,461,964,813) |

- **O1** (TM1): KCHECK at 10¹⁰ `13950685721272283034 5849625012 11`, at 1.08·10¹⁰ `11135687718517257442 6317595012 11`. An independent run reproduces the KCHECK values at 6·10⁸ … 10⁹ (`8610941070033361538 584962505 1101`) and, continued to Bell 1,000,000,005, the reference value `825729492582408624 584962508 10001` of the TM1 repository. **Ersen reached 10¹¹** (22 Oct) with his own engine (divide and conquer, C++ leaf, GMP, FLINT multiplication, horizon pruning towards 10¹¹, resumed from his checkpoint at Bell 2,671,088,640): no halt, final KCHECK `8917149296721920962`, S = `11` (bit length pruned; full precision up to about 6.3·10¹⁰). His pure-GMP and FLINT engines agree in KCHECK, bit length and S at all 41 milestones from 3·10⁹ to 4.3·10¹⁰; his value at 10¹⁰ is exactly the `bellntt` value above (`13950685721272283034 5849625012 11`), an independent confirmation; at 3·10⁹ … 6·10⁹ his values are `8175196542158952476 1754887506 10001`, `5510212674155588110 2339850007 11`, `919453248881081670 2924812508 1101`, `14477254705213975050 3509775009 10001`. A `belldco` run from Bell 1,000,001 reproduces these four values exactly (KCHECK, bit length and S).
- **O2** (TM2, TM1-F, TM2'): two independent programs, Ersen's engine (GMP, divide and conquer) and `belldc` (Thomas Reus, horizon pruning towards 10¹¹), agree in KCHECK and S at all 17 common checkpoints from 2·10¹⁰ to 10¹¹ (every 5·10⁹; also in the bit length up to 6·10¹⁰, the end of the full-precision range). At 10¹¹: KCHECK `6379036783869152234`, S = `11`. Earlier: `bellntt` to 2·10¹⁰ (equal to Ersen at 1.9·10¹⁰ and 2·10¹⁰ including bit lengths: `12174170564911698608 11699250019 1` at 2·10¹⁰), a second-computer run to 1.7·10⁹ (17 checkpoints), and Andrew Ducharme at 3.5·10⁹ (`283842985451259460 2047368757 1`). `belldc` run time from 8.5·10⁹ to 10¹¹: 16 hours on a notebook (16 GB RAM). Continued to **1.4·10¹¹** (pruned run towards 1.4·10¹¹ from 5·10¹⁰, 23 Oct): KCHECK `37654335792028544`, S = `1101`; D = 3 at Bell 139,153,319,148, i.e. the orbit came within 3 Bells of a HALT entry of the table (D was 5 before). The exact checkpoint at 8·10¹⁰ (the end of the full-precision range for this target) is kept, so the orbit can be continued beyond 1.4·10¹¹ from there. **Continued with `belldco`** from that checkpoint (run towards 7·10¹¹, started 23 Oct): at 10¹¹, 1.2·10¹¹ and 1.4·10¹¹ it gives exactly the same KCHECK and S as the earlier `belldc` runs (now with full bit lengths, e.g. `6379036783869152234 58496250077 11` at 10¹¹), it reached 1.6·10¹¹ on 24 Oct (KCHECK `12452894743089909202 93594000120 111`) 2.8·10¹¹ on 25 Oct (KCHECK `1789886949569951688 163789500206 10001`) and **3.6·10¹¹** on 26 Oct (KCHECK `9478173992275604592 210586500264 11`), no halt; D is still 3. Further checkpoints: 3·10¹¹ `4051791190435406468` S = `11`, 3.2·10¹¹ `30401007762574222` S = `1`, 3.4·10¹¹ `18253871615987621126` S = `11`. Then 3.8·10¹¹ `14576138855366184346` S = `10001`, 4·10¹¹ `13416445904600297320` S = `1`, and **4.2·10¹¹** on 27 Oct (`11078700321512525134 245684250307 11`, still full precision). From this exact checkpoint the run was restarted on 27 Oct with the **new target 10¹²** (`belldco -t 1000000000000 -p -M 8 -j auto -i 20000000000`). Checkpoints since 1.6·10¹¹: 1.8·10¹¹ `2903132793933580804` S = `10001`, 2·10¹¹ `5317274857225906556` S = `1`, 2.2·10¹¹ `17534791635571930592` S = `1`, 2.4·10¹¹ `12628327662601704012` S = `10001`, 2.6·10¹¹ `766523030864727157` S = `1`. Expected end at 10¹²: about 5–6 Nov (the intervals grow until pruning takes over at about 6.3·10¹¹ and shrink after that). Speed: 2·10¹⁰ Bells in 2.4–3.1 hours at k ≈ 6–9·10¹⁰ bits 5.4 hours at k ≈ 1.6·10¹¹ bits and 7.2 hours at k ≈ 2.1·10¹¹ bits (8 threads, 8 GB RAM); about 1060 s + 1.1·10⁻⁷ s per bit of k per 2·10¹⁰ Bells.
- **O3** (TM2a): Ersen reached 10¹¹ (final KCHECK `9899542532481302830`, S = `11`, pruned run; full precision up to 6.3·10¹⁰). At 10¹⁰ three programs agree: Ersen, Andrew Ducharme (`bellntt`) and `belldc`, KCHECK `9939947858229016780`; Ersen and Andrew also agree at 1.3·10¹⁰ and 1.4·10¹⁰, and `belldc` reproduces Ersen's values at 10⁸ … 5·10⁸. **Duke** started a `belldcf` run towards 10¹² on 26 Oct (cluster computer, plenty of RAM, more than 4 TB disk); his KCHECK values agree with Ersen's. He reached **1.7·10¹¹** on 26 Oct (KCHECK `17154956848195521320 99443625127 11`, full precision), no halt. On the way the orbit came within 3 Bells of a HALT entry: D = 3 at Bell 112,674,809,806 (before: D = 9 at Bell 420,738,969).
- **O4** (TM2b, TM2b'): Andrew Ducharme reached 10¹⁰ with `bellntt` (KCHECK `281319679749230232 5849625012 1100001`), reproduced exactly by `belldc`; with `belldc` he reached 10¹¹ on 22 Oct, 1.25·10¹¹ on 24 Oct and **1.75·10¹¹** late on 24 Oct (KCHECK `10679250096216309968 102368437631 1101`, full precision), and **2.25·10¹¹** on 25 Oct, no halt. At 2.25·10¹¹ the checkpoint (about 33 GB) could not be written and the program stopped before logging, so there is no KCHECK for it. The closest approach is D = 5 at Bell 126,461,964,813 (before: D = 6 at Bell 2,129,211,986).
- In pruned runs only the low part of k is kept, so beyond 0.63·T only KCHECK = k mod 2⁶⁴ and S are compared, not the bit length.
- **Next:** all four orbits are now at 10¹¹ or beyond. Beyond 1.4·10¹¹ on a 16 GB computer: `belldco` (k on disk, see below); a pruned run to 7·10¹¹ needs about 200 GB of free disk space, to 10¹² about 280 GB.
- **Halting probability** (Markov estimate, see [below](#halt-expected-markov-estimate)): up to Bell 10¹¹ about 8.5 % per orbit (30 % for at least one of the four orbits), up to 10¹² about 59 % per orbit (97 % for at least one); the value for four orbits assumes that they behave like independent random sequences.

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

### Horizon pruning and `bellnttp`
**Idea** (used by Ersen for his O2 run to 10¹¹): the next Bell depends only on S and k mod 4, and k' = 3·⌊k/2⌋ + c, so k' mod 2<sup>j</sup> depends only on k mod 2<sup>j+1</sup>. To decide whether an orbit halts before a target Bell T, it is enough to keep k mod 2<sup>(T − N) + margin</sup> at Bell N instead of the whole k. Up to N ≈ 0.63·T the whole k is shorter than that and nothing changes; after that the number shrinks towards T. KCHECK = k mod 2⁶⁴ and S stay exactly comparable with full runs; only the bit length differs.

**Memory.** The largest number of a pruned run has about 0.37·T bits instead of 0.585·T:

| target T | largest k, full run | largest k, pruned run | RAM, pruned run with `bellnttp` (estimate) |
|---|---|---|---|
| 2·10¹⁰ | 1.5 GB | 0.9 GB | ~5 GB |
| 4·10¹⁰ | 2.9 GB | 1.8 GB | ~9 GB |
| 10¹¹ | 7.3 GB | 4.6 GB | ~25 GB |
| 10¹² | 73 GB | 46 GB | ~250 GB (or RAM + disk) |

**Run time.** With `bellntt`'s block method the part up to 0.63·T costs as much as before, the pruned part much less; a pruned run to T takes roughly 0.6–0.8 of a full run to T (measured: 0.8 at T = 6·10⁷). The large speed-up of Ersen's engine (about 3–4 minutes per 10⁹ Bells at 2·10¹⁰ bits, roughly 30–100 times faster than `bellntt` there) comes from its divide-and-conquer multiplication with GMP, not from the pruning.

**Limit.** A pruned run cannot be continued beyond its T, since the upper bits are gone. To go further, a new run has to start from a full checkpoint at Bell ≤ 0.63·T (or from Bell 5).

**`bellnttp`** (in each orbit directory) is `bellntt` with two additions:
- option `-p` (with `-t T`): horizon pruning towards T, keeping (T − N) + 128 bits. Pruned checkpoints are written as `bell_<N>_pchkpt.txt` with a line `horizon T`; `bellntt` does not read them, and `bellnttp` uses them only with `-p` and a target ≤ T. Without `-p`, `bellnttp` works exactly like `bellntt` and uses the same checkpoints.
- **D, the distance to HALT.** For every word S of the table, d(S) is the smallest number of Bells after which a HALT entry can be reached from S if the bits of k are suitable (d = 1: the next Bell can halt; for the TM1 table d lies between 1 and 44). Each log line shows d(S) at the checkpoint and D = the smallest d reached at any Bell so far, with the Bell where it happened (stored in the checkpoints; for runs continued from older checkpoints, tracking starts there). A path of length d needs about d suitable bits of k, i.e. it has a probability of roughly 2<sup>−d</sup>, so D shows how close the orbit has come to a halt. Example: O1 from Bell 10⁶ to 10⁷ reaches D = 15 (at Bell 1,056,246), O2 in the same range D = 19.

Tests: pruned and full runs give identical KCHECK and S at every checkpoint (O1 to 10⁷, including the TM1 reference value at 10,000,005; O2 to 6·10⁷, equal to the values of the main O2 run); a pruned run interrupted and continued gives the same result; a pruned checkpoint is refused for a run without `-p` or with a larger target.

### `belldc`: divide and conquer with GMP
`belldc` (in each orbit directory) computes the same orbit much faster. It uses the same block idea as `bellntt` (k = q·2<sup>B+2</sup> + r; after B Bells k = q·3<sup>B</sup>·4 + r<sub>B</sub>), but computes the low part r<sub>B</sub> **recursively**: B Bells = B/2 Bells on the lowest B/2 + 2 bits, one product with 3<sup>B/2</sup>, then B/2 Bells on the result; only blocks of at most 32 Bells are simulated directly, on a 64-bit word. The cost grows like N·log²N instead of N<sup>1.5</sup>. All multiplications use GMP (one core). It has the same options as `bellnttp` (`-t`, `-p`, `-i`, `-b`) plus `-m` (memory saving), the same checkpoint files (the programs can continue each other's runs) and the same log lines, including D.

    sudo apt install -y libgmp-dev
    gcc -O3 -march=native -o belldc belldc.c -lgmp
    ./belldc -t 20000000000 -i 1000000000          # add -p for horizon pruning, -m to save memory

Measured on 1 core (cloud machine), orbit O2:

| range | `bellntt` (2 threads) | `belldc` | `belldc -m` | peak memory `belldc` / `-m` (k at the end: 292 MB) |
|---|---|---|---|---|
| Bell 10⁶ → 1.7·10⁹ | 4,188 s | 391 s | – | – |
| Bell 1.7·10⁹ → 4·10⁹ | ≈ 9,000 s (notebook) | 755 s | 1,228 s | 1.05 GB / 0.47 GB |

So `belldc` is about 10–12 times faster than `bellntt` at these sizes, and the factor grows with N (about 4–5 minutes per 10⁹ Bells at k ≈ 2·10⁹ bits). Its memory is about 3.6 × the size of k, with `-m` about 1.6 × (and about 1.6 times slower).

Rough estimates for a notebook with 16 GB RAM (WSL set to about 13 GB with `memory=13GB` in `.wslconfig`): full runs up to about 5·10¹⁰ (`-m`: about 10¹¹); pruned runs (`-p`) up to about 8·10¹⁰ (`-m`: about 1.5·10¹¹). Run time to 10¹⁰ about 1 hour, to 10¹¹ (pruned) about half a day to one day. Note the size of the checkpoint files (one hex digit per 4 bits of k): e.g. 9 GB at k = 3.7·10¹⁰ bits (the largest k of a pruned run to 10¹¹); for such runs choose a large interval (`-i 5000000000`) and keep enough free disk space for two checkpoints.

Tests: `belldc` reproduces the KCHECK values of `bellntt` at every checkpoint (O1 to 10⁷ including the TM1 reference, O2 at all 17 checkpoints from 10⁸ to 1.7·10⁹ and at 2·10⁹, 3·10⁹, 4·10⁹); its checkpoints are identical to those of `bellntt` (same k and checksum, checked at Bell 10,000,005), pruned ones to those of `bellnttp` (checked at 6·10⁷); runs continue across the programs; a HALT inside the recursion is found at the same Bell as with `bellnttp` (test with an artificial start).

### `belldcf`: `belldc` with FLINT on several cores
`belldcf` (in each orbit directory) is `belldc` with two changes; the orbit, the checkpoints and the log lines are the same, so the programs can continue each other's runs.

- The big multiplications use FLINT's `fft_small` multiplication (`flint_mpn_mul`), which is faster than GMP already on one core and runs on up to 8 threads per product.
- The product of the high part with 3^h does not depend on the Bells on the low part, so for large numbers it runs in a second thread while the low part is advanced. This happens both at the top level, where q·3^B runs during the B Bells on r, and inside the recursion.

Option `-j N` sets the number of threads; the default is all cores. With `-j auto` the program uses the cores that other programs leave free, measured from the 1-minute load average before each block and at most once a minute; `-j auto:MAX` caps this at MAX threads.

Installation and start (needs FLINT ≥ 3.0 with `fft_small`, which is built automatically on x86-64 with AVX2):

    sudo apt install libflint-dev          # Ubuntu 24.04; if the build below fails, build FLINT from source (next lines)
    # sudo apt install build-essential autoconf automake libtool libgmp-dev libmpfr-dev git
    # git clone --depth 1 --branch v3.4.0 https://github.com/flintlib/flint && cd flint
    # ./bootstrap.sh && ./configure && make -j8 && sudo make install && sudo ldconfig && cd ..
    gcc -O3 -march=native -o belldcf belldcf.c -lflint -lmpfr -lgmp -lpthread -lm
    ./belldcf -t 140000000000 -p -m -i 10000000000 -j 8

Measurements: O2, 2 cores, FLINT 3.4.0. k at the end is 292 MB. All times are from the same machine; for `belldc -m` on the long range the time is estimated from its ratio to `belldc` at smaller k (1.75). The memory values for `belldc` are from the table above.

| range | `belldc` | `belldc -m` | `belldcf -m -j 2` | peak memory `belldc` / `belldc -m` / `belldcf -m` |
|---|---|---|---|---|
| Bell 1.3·10⁹ → 4·10⁹ | 977 s | ≈ 1,700 s | **482 s** | 1.05 GB / 0.47 GB / 0.63 GB |
| Bell 10⁶ → 5·10⁸, pruned (`-p -m`) | – | 167 s | **62 s** | – |

With `-m`, `belldcf` is about 3 times as fast as `belldc -m` on 2 cores. It needs about 2.2 × the size of k in memory, against 1.6 × for `belldc -m`. That memory includes freeing FLINT's FFT buffers after every block and returning freed memory to the system at once. Without `-m`, `belldcf` is a little faster but needs about 7 × k. More cores should give more speed, but not linearly: the bottom of the recursion, at most 32 Bells on a 64-bit word, stays sequential. Measurements on 4–8 cores are still missing.

Tests: `belldcf` gives the same KCHECK, bit length and S as `belldc` at all compared checkpoints (O2: 3·10⁸, 1.3·10⁹, 4·10⁹; pruned towards 5·10⁸; with `-j 1`, `-j 2` and `-j auto`), and finds a HALT at the same Bell (artificial start).

### `belldco`: k on disk (out of core)
`belldco` (in each orbit directory) removes the memory limit. The number k stays on disk as a binary file; only the parts needed for one block of Bells are in RAM. The orbit, the checkpoints and the log lines are the same as in `belldc` / `belldcf`; a checkpoint written by `belldco` is byte for byte the same as one written by `belldc`, apart from the date, time and program lines.

How one block of B Bells works, with k = q·2<sup>B+2</sup> + r:
- **Streamed product (own thread).** q is read from the work file in pieces. Each piece is multiplied by 3<sup>B</sup> in RAM with FLINT, and the result is written in order to a second work file. The upper part of each piece's product is carried into the next one.
- **Low part (main thread, at the same time).** The B Bells on r are computed in RAM, as in `belldcf`.
- **Finish.** r<sub>B</sub> is added at the bottom of the new file.

So each block reads k once and writes it once. With pruning, only the part of the product below 2<sup>keep</sup> is computed and written.

    gcc -O3 -march=native -o belldco belldco.c -lflint -lmpfr -lgmp -lpthread -lm      # needs FLINT >= 3, see belldcf
    ./belldco -t 1000000000000 -p -M 8 -j 8 -i 20000000000

- `-M GB`: memory budget for the parts in RAM (default 4). It sets the largest block, GB·2³⁰/6 Bells; measured peak memory is about 5 bytes per Bell of a block, so the peak stays near the budget. It does **not** depend on k.
- `-w DIR`: directory for the two work files (default: the current directory). Each work file is as large as k; for a pruned run to 10¹² the largest k, at Bell ≈ 6.3·10¹¹, is about 46 GB.
- Disk space for a run to 10¹²: the two work files plus the checkpoints. Checkpoints are hex text, twice the size of k; the start checkpoint, the newest one and with `-p` the last exact one are kept, so allow about 400 GB.
- `-j`, `-t`, `-p`, `-i`, `-b` work as in `belldcf`.

**Checkpoint size and a full disk** (all three programs, since 25 Oct).
- **Size.** A full-precision checkpoint at Bell N holds about 0.585·N bits of k as hex text, i.e. about 0.15·N bytes: 15 GB at 10¹¹, 33 GB at 2.25·10¹¹. While the new one is written, the previous one still exists, so about twice that is needed. With `-p` the size is at most 0.37·T bits (at Bell ≈ T/1.585) and then shrinks.
- **Log line first.** The log line with KCHECK is now written to `progress.log` *before* the checkpoint.
- **Failed write.** If the checkpoint cannot be written (disk full), the program reports it in the log, removes the partial file, keeps the previous checkpoint and **continues**. Only at the target Bell does it stop with an error.
- **Test.** Checked with a checkpoint redirected to `/dev/full` (O4, Bells 10⁶ … 3·10⁷, `belldc`, `belldcf` and `belldco`): the KCHECK values are logged and the run continues to the target.

Measurements (O2, 2 cores, same range as above, k at the end 292 MB):

| range | `belldc` | `belldcf -m -j 2` | `belldco -M 0.25 -j 2` | `belldco -j 2` (default `-M 4`) |
|---|---|---|---|---|
| Bell 1.3·10⁹ → 4·10⁹ | 977 s | 482 s | **400 s** | 474 s |
| peak memory | ≈ 1.05 GB | 0.63 GB | **0.42 GB** | 1.36 GB |

Smaller blocks are not slower here, because the streamed product runs in parallel with the low part. For very large k the streamed product becomes the larger part, since it reads and writes all of k once per block; then larger blocks, i.e. a larger `-M`, pay off.

Tests: same KCHECK, bit length and S as `belldc` / `belldcf` at 3·10⁶, 3·10⁸ and 4·10⁹, with block sizes 999, 1,234,567 and automatic, with `-M 0.25` and `-M 4`. A pruned run towards 5·10⁸ gives the same result as `belldc -p` and keeps the exact checkpoint at 3·10⁸. Checkpoints of `belldc`, both exact and pruned, are read, and the written checkpoints are identical to those of `belldc`. A HALT is found at the same Bell (artificial start).

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
A quick scan of the 663 BB(6) holdouts (`scan/holdouts_663.txt`) for Bell behaviour (`scan/bellscan.c`, 10⁷ steps per machine) found 56 machines with Bell-like growth (`scan/bell_candidates.txt`; with level analysis and a space-time diagram for each machine: [`scan/bell_candidates.md`](scan/bell_candidates.md)).
Seven of them (class A) grow very regularly by a factor of about 1.56 per Bell; these are the seven machines above. The other 49 grow with other factors or less regularly and have not been analysed.

## Open points
- The identifications are observations from simulations and tables (checked for finitely many cases), not proofs.
- Markov estimate for the orbits O3 and O4 not recomputed (expected: the same as for TM1/TM2).
- Long simulations: O2 is at 4.2·10¹¹ Bells, O3 at 1.7·10¹¹, O1 at 1.08·10¹⁰, O4 at 10¹⁰ (see the simulation status at the top); O1 and O4 still to be taken to 10¹¹.
- **From a HALT to a Coq proof.** If an orbit reaches a HALT entry, a formal proof would consist of (1) the Turing machine semantics (available from the bbchallenge Coq work), (2) the few steps from the blank tape to the first Bell, (3) one lemma per table entry, `0^∞ 1^k F> S 0^∞` → `0^∞ 1^(3⌊k/2⌋+c) F> S' 0^∞` for all k by induction (several thousand lemmas, but uniform, so the proof scripts can be generated from the table), (4) the reduction "the machine halts iff the iterated Bell map reaches HALT", and (5) the computation of the orbit up to the halting Bell. Parts (1)–(4) look feasible; part (5) is the open problem: about 10¹² iterations with numbers of up to ~10¹¹ bits are far beyond what Coq can compute itself, and the orbit is pseudo-random, so there is no closed formula to shortcut it. A realistic route would be a Coq proof of (1)–(4) together with the computation done outside Coq by at least two independently written programs on different computers, agreeing in their checkpoint values (KCHECK); whether bbchallenge accepts such a combined proof is to be asked. A halt after roughly 10^(10¹¹) steps would not be a new BB(6) record, but it would decide every machine of the family on the halting orbit.

## Files
| Path | Content |
|---|---|
| `orbits/O1` … `orbits/O4` | fast simulation (`bellntt`; `bellnttp` with horizon pruning and distance to HALT; `belldc`, divide and conquer with GMP, about 10 times faster; `belldcf`, the same with FLINT on several cores; `belldco`, with k on disk, memory independent of k) of one orbit each, with table and checkpoints; each directory can be copied and used on its own |
| `TM2.md` | detailed notes on TM2 (table, Markov estimate, Discord history) |
| `src/cyc.c` | Bell simulator for the TM2-type machines: direct simulation, and single Bells from a given (P, n) |
| `src/table.py` | builds a table by breadth-first search with `cyc` |
| `src/compare.py` | the checks behind this document: machine core, tables against TM2, orbits |
| `tables/TM2.json`, `TM2a.json`, `TM2b.json` | tables of TM2, TM2a, TM2b (about 3,000 words each) |
| `scan/bellscan.c`, `scan/bell_candidates.txt`, `scan/holdouts_663.txt` | Bell detector, its results, and the list of holdouts it was run on |
| `scan/bell_candidates.md`, `scan/diagrams/`, `scan/viz.c` | the 56 candidates with classification, level analysis, verdict and a space-time diagram each |

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
