# bb6: does this 6-state Turing machine halt on the empty tape? (TM2)

    1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---

Open question: does the machine ever halt? It is known in the bbchallenge community as an "energy vampire" and is believed to be *probviously halting*
(it halts with probability 1 under a heuristic model), but that has not been proved, and the orbit has not been simulated up to a halt.
This document collects what is known and the results of our own investigation. It is a draft; programs and tables are not published yet.

> **Remark (16 Oct 2026): a mirror-image sister machine.** The machine `1RB---_1LC0RB_0LD0LC_1RE1RB_1RD1LF_1LA0LE` (TM1, see the repository [bb6-1RB---_1LC0RB_0LD0LC_1RE1RB_1RD1LF_1LA0LE](https://github.com/thomasreus-bb/bb6-1RB---_1LC0RB_0LD0LC_1RE1RB_1RD1LF_1LA0LE)) has the same kind of cycles ("Bells"), and its tape looks like a mirror image of this one:
> here the growing `(10)^n` part lies on the left and the block of ones that is used up during a cycle on the right; in TM1 it is the other way round.
> Their tables correspond by S<sub>TM1</sub> = `11` + (P<sub>TM2</sub> read backwards) and k = 2n, and the Markov estimates agree (see "Relation to TM1" below).
> In a quick direct simulation (2·10⁷ steps each) the block lengths at the start of the cycles grow almost in parallel, by a factor of about 1.56 per cycle in both machines.
> This is an observation only, not a proof; the two machines are not exact mirror images of each other, and their orbits differ. A joint analysis may follow later.

## Idea in brief
The only halting transition is F reading 1. The machine runs in cycles. Each cycle ends when the head enters state F at the right end of the tape:

    0^∞  P  (10)^n  11  F>  0^∞        (n maximal, so P does not end in 10)

Here P is a short word (empty or starting with 1), n is a large number, and F reads a 0, so the machine goes on. The next cycle ends in

    n' = (3n + d) / 2 ,        (P', d) = f(P, n mod 2)

or in HALT, if during that cycle F reads a 1. d is a small constant (5 to 35 in our table); 3n + d is always even.
So the machine acts like a Collatz/Hydra-type map on n, while the word P performs a random-looking walk driven by the parity of n.

Example: P = `1000`, n = 1,012 (even): f(`1000`, 0) = (`101`, 8), so n' = (3,036 + 8)/2 = 1,522 and P' = `101` (cycles 12 → 13 below).

The number of TM steps in one cycle is a quadratic polynomial in n:

    t' = t + (3/2)·n² + β·n + γ

with β, γ depending on P and n mod 2. This was found by direct simulation: for 7 words P (ε, `1`, `1000`, `101`, `11000`, `11`, `1101`) and both parities,
n = 80 … 95, the second difference is always 12 (leading coefficient 3/2), and β, γ were positive in all of these cases (β between 13 and 25).
Example: P = `1000`, n = 1,012 even: 3/2·1,012² + 22·1,012 + 47 = 1,558,527, exactly the difference of t between cycles 12 and 13 below.
For other words and larger n this is an extrapolation, not a proof.

**Notation in the Discord thread.** The thread uses f(S, n) := 0^∞ S (10)^n 111000 C> 0^∞, start f("", 2) (Peacemaker II). That is a different point in the same cycle.
The words agree (S = P), but the parity of n is swapped: for every rule we compared, their "n even" is our "n odd" and vice versa.

## The first 24 cycles
Direct simulation (about 2·10¹⁰ TM steps, 2 minutes). `t` = number of TM steps up to the end of the cycle (the F entry), `n` and `P` as above, `d` = constant of the transition to the next cycle, i.e. n<sub>i+1</sub> = (3·n<sub>i</sub> + d<sub>i</sub>)/2.

| i | t (steps) | n | n mod 2 | P | d |
|---:|---:|---:|---:|---|---:|
| 1 | 27 | 3 | 1 | ε (empty) | 11 |
| 2 | 178 | 10 | 0 | ε (empty) | 8 |
| 3 | 595 | 19 | 1 | `1` | 5 |
| 4 | 1,534 | 31 | 1 | `1000` | 11 |
| 5 | 3,813 | 52 | 0 | `1` | 8 |
| 6 | 8,738 | 82 | 0 | ε (empty) | 8 |
| 7 | 20,675 | 127 | 1 | `1` | 5 |
| 8 | 47,318 | 193 | 1 | `1000` | 11 |
| 9 | 108,079 | 295 | 1 | `1` | 5 |
| 10 | 244,258 | 445 | 1 | `1000` | 11 |
| 11 | 552,483 | 673 | 1 | `1` | 5 |
| 12 | 1,244,700 | 1,012 | 0 | `1000` | 8 |
| 13 | 2,803,227 | 1,522 | 0 | `101` | 8 |
| 14 | 6,302,346 | 2,287 | 1 | `1` | 5 |
| 15 | 14,191,389 | 3,433 | 1 | `1000` | 11 |
| 16 | 31,955,510 | 5,155 | 1 | `1` | 5 |
| 17 | 71,914,529 | 7,735 | 1 | `1000` | 11 |
| 18 | 161,853,304 | 11,608 | 0 | `1` | 8 |
| 19 | 364,157,565 | 17,416 | 0 | ε (empty) | 8 |
| 20 | 819,516,348 | 26,128 | 0 | `1` | 8 |
| 21 | 1,843,943,009 | 39,196 | 0 | ε (empty) | 8 |
| 22 | 4,149,294,992 | 58,798 | 0 | `1` | 8 |
| 23 | 9,336,043,003 | 88,201 | 1 | ε (empty) | 11 |
| 24 | 21,007,372,692 | 132,307 | 1 | ε (empty) | |

**Macro simulation.** Iterating n' = (3n + d)/2 with a table of f gives the sequence of cycles without simulating the tape.
It reproduces all 24 cycles above (n and P) and was run to 10⁶ cycles (26 s in Python).

## The table f
f was computed by direct simulation: for each word P and each parity the machine was started in 0^∞ P (10)^n 11 F> 0^∞ with three values of n of that parity
(n of about 2·|P| + 12, spaced by 2, so that n mod 4 also varies), run to the next F entry at the right end of the tape, and the result was accepted only if all three runs gave
the same P' and the same d (or all three halted). F entries in the middle of the tape (they occur, e.g. for P = `11111`) are passed over; if F reads a 1 there, the entry is HALT.

The table holds the words reachable from the start, found by breadth-first search: 49,993 words (about 100,000 entries, words up to 25 symbols), 810 of them HALT entries.
The set of reachable words is not closed (hipparcos, Discord, Aug 2025); the table is a finite part of an apparently infinite graph.
Words never end in `10` (that would be part of (10)^n). Excerpt (ε = empty word):

| P | n even → P', d | n odd → P', d |
|---|---|---|
| ε | `1`, d=8 | ε, d=11 |
| `1` | ε, d=8 | `1000`, d=5 |
| `11` | `100`, d=8 | ε, d=7 |
| `100` | `11`, d=8 | `1`, d=11 |
| `101` | `1`, d=8 | `11000`, d=5 |
| `111` | ε, d=8 | ε, d=9 |
| `1000` | `101`, d=8 | `1`, d=11 |
| `1101` | ε, d=14 | `1000000`, d=5 |
| … | | |
| `1111` | ε, d=8 | HALT |
| `11111` | HALT | `101011`, d=7 |
| `111101` | ε, d=10 | HALT |
| `1111011` | HALT | `10101011`, d=7 |

## HALT expected! (Markov estimate)
This is a heuristic, not a proof.

**Reasoning.** P' and HALT depend only on P and on n mod 2 (checked with three values of n per entry). Assume that the parity of n behaves like a fair coin in every cycle.
Then the sequence of words is a Markov chain on the words of the table: each word has two successors with probability 1/2 each, and a HALT entry ends the chain.
(Keeping the lowest bits of n exactly and refilling random bits on top, as in hipparcos' Monte Carlo runs, gives the same model: the map n → (3n + d)/2 permutes the residues of the low bits, so uniformly random low bits give independent fair parities.)

- **Visit frequencies agree with the real orbit.** Over the first 10⁶ cycles of the real orbit the total variation distance to the model is 0.0013;
  the three most frequent words ε, `1`, `1000` occur with frequencies 0.3467, 0.2980, 0.1535 (model: 0.3458, 0.2977, 0.1538).
  The word `100100101` occurs once in 2.12·10⁸ cycles in the model, the same value LegionMammal978 found on Discord (Sep 2025).
- **Halt rate.** The halt probability per cycle is **8.87·10⁻¹³**. Expected number of cycles until the halt, starting from cycle 1: **1.127·10¹²**, median about 7.8·10¹¹.
  The halt comes through the word `1111` (n odd) with probability 61.4 % and through `111101` (n odd) with 38.6 %; all other HALT entries together contribute less than 10⁻⁵.
- **Size of the table.** With 2,000, 20,000 and 100,000 entries the expected value is the same to 4 digits, and the probability of leaving the table before the halt is negligible
  (about 2·10⁻⁶). The value was computed in two ways (direct solve of the absorbing chain, and via excursions from the start word) with the same result.

| cycles N | P(halt up to N) |
|---|---|
| 10⁹ | 0.089 % |
| 10¹⁰ | 0.88 % |
| 10¹¹ | 8.5 % |
| 10¹² | 58.8 % |
| 2·10¹² | 83 % |
| 5·10¹² | 98.8 % |
| 10¹³ | 99.99 % |

**Comparison with the estimates on Discord.**
- LegionMammal978 (Sep 2025): ≈ 6.95·10¹² steps, from the frequency of `100100101` and the 15-step main path from there to the halt. Only that one path is counted, so the value is too high.
- hipparcos (Sep 2025): 20 Monte Carlo runs, all halted, mean 5.9·10¹¹ steps (between 2.1·10⁹ and 2.0·10¹²), 13 on `1111` and 7 on `111101`.
  The shares fit our 61 % / 39 %. The mean is lower than ours by about a factor 2; if our value is right, a mean this low over 20 runs has a probability of only about 1 %. The reason is not known.

**Limits.** The fair-coin assumption is not proven: the bits of n come from the 3/2 dynamics, so correlations are possible, and they could change all the numbers above
(even whether a halt ever happens). The table rules were checked for three values of n each, not proved for all n.

## Relation to TM1
TM1 = `1RB---_1LC0RB_0LD0LC_1RE1RB_1RD1LF_1LA0LE` (our other investigation) has, as far as we can see, the same dynamics as TM2:

- Its table maps onto the table of TM2 by S<sub>TM1</sub> = `11` + (P<sub>TM2</sub> read backwards) and k = 2n. Examples: ε ↔ `11`, `1` ↔ `111`, `1000` ↔ `110001`, `101` ↔ `11101`; the HALT words `1111` ↔ `111111` and `111101` ↔ `11101111`.
- Of the 91,130 entries that can be compared, 83,324 match directly. The others differ only in how the cycle boundary is encoded (in TM1 the chosen Bell start then has an odd k, or lies inside a descent).
- The Markov estimates agree: halt rate 8.87·10⁻¹³, expected 1.13·10¹² steps, halt shares 61.4 % / 38.6 %, visit frequencies 0.3457 / 0.2977 / 0.1538.

However, the two machines start differently, and their orbits are not the same (TM1, Bell 9: k = 524; TM2, cycle 9: n = 295). So TM1's simulation to 10⁹ Bells without a halt says nothing directly about TM2's orbit.
The correspondence is an observation from the tables, not a proof.

## Memory demand
n grows by a factor of about 3/2 per cycle, so after N cycles it has about N·log₂(3/2) = 0.585·N bits (cycle 24: n = 132,307, 17 bits; after 10⁶ cycles: 584,967 bits).

**Lower bound for the number of TM steps.** If a cycle with parameter n takes at least 3/2·n² steps (β, γ ≥ 0, checked only for the words listed above) and n' ≥ 1.5·n (true, since every d in the table is at least 5),
then t<sub>N</sub> ≥ t<sub>24</sub> + 3/2·n<sub>24</sub>²·Σ 2.25<sup>j</sup> ≈ 2·10¹⁰·2.25<sup>N−24</sup> = 10<sup>0.352·N + 1.9</sup>.

| cycles N | n | memory for n | TM steps t, lower bound |
|---|---|---|---|
| 10⁹ | 585 million bits | 73 MB | 10<sup>3.52·10⁸</sup> |
| 10¹⁰ | 5.85 billion bits | 0.73 GB | 10<sup>3.52·10⁹</sup> |
| 10¹¹ | 58.5 billion bits | 7.3 GB | 10<sup>3.52·10¹⁰</sup> |
| 10¹² | 585 billion bits | 73 GB | 10<sup>3.52·10¹¹</sup> |

## Fingerprints of the orbit
State after N applications of f, starting from cycle 1 (P = ε, n = 3), i.e. at the end of cycle N + 1: `n mod 2⁶⁴`, bit length of n, P.

| N | n mod 2⁶⁴ | bits | P |
|---|---|---|---|
| 10⁴ | 10344533065338383136 | 5,854 | ε |
| 10⁵ | 11927179264807263660 | 58,500 | `11` |
| 10⁶ | 16065736760597740477 | 584,967 | ε |

(Computed only with our Python macro simulation, not yet cross-checked.)

## Earlier work (bbchallenge Discord)
Thread "(probviously halting?) 1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---" in the bbchallenge Discord, July 2025 to July 2026:
- Peacemaker II: notation f(S, n), first rules, and the main path of about 40 rules from ε to f(`1111`, even) → HALT.
- Shawn Ligocki: the name "energy vampire". LegionMammal978: the attractors ε and `1`, frequency of `100100101`, estimate of 6.95·10¹² steps / 473 GiB, an mpn-based Hydra program.
- hipparcos: the set of words is not closed, many HALT words, Monte Carlo runs (see above), code: [github.com/jhuang97/turing_machine](https://github.com/jhuang97/turing_machine) (`src/bin/bb6_vampire.rs`, `src/definitions/bb6_vampire.txt`).
- dyuan01: a simple procedure to derive the rules from S. Katelyn Doucette: simulator [github.com/Laturas/mildly_upsetting_tm_simulator](https://github.com/Laturas/mildly_upsetting_tm_simulator).
- Status in July 2026: no simulation up to a halt yet; estimates of the memory needed ranged from tens of GB to about 1 TB. (A remark in the thread mentions a run to 469 billion steps of the rule map; we have not checked this.)

## Status (15 Oct 2026)
- Direct simulation up to cycle 24 (2·10¹⁰ TM steps), macro simulation up to 10⁶ cycles, no HALT.
- Heuristic only, not a proof: halt rate about 8.9·10⁻¹³ per cycle, expected about 1.1·10¹² cycles, P(halt by 10¹²) ≈ 59 %.
- The dynamics appear to be the same as for TM1.

## Next steps
- Adapt the fast simulation of TM1 (block method with NTT) to TM2 and cross-check the fingerprints above.
- Publish the table and the programs.
- Clarify the factor 2 between our estimate and hipparcos' Monte Carlo mean.

This investigation was made together with the AI model Claude Opus 5.5. An independent review would be desirable.

## Files (internal, not yet published)
| File | Content |
|---|---|
| `derive2.c` | derives entries of f by direct simulation (three values of n per entry) |
| `graph.py` | builds the table by breadth-first search and solves the Markov chain |
| `macro.py` | macro simulation of the orbit with the table |
| `cycles.c` | direct simulation, prints the end of every cycle |

## License
MIT
