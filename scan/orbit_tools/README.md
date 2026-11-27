# Exact event orbits with learned affine rules (27 Nov 2026)

Generic tools used for the analyses of nos. 82, 83 and 107 (see `scan/m82`, `scan/m83`, `scan/m107`).
The scripts were run from `/tmp/an/`; the paths `/tmp/an/...` are hard-coded and must be adapted.

| file | purpose |
|---|---|
| `raw.c` | `raw TM N [side]`: at every new left record print step, state and the raw tape (0/1) |
| `rlev.c` | `rlev TM N SIDE MINSTEP`: the same as run lengths, left/right/both records |
| `synth.c` | `synth TM q headoff maxsteps`: run from a tape given on stdin until the next left record (or HALT) |
| `synthev.c` | like `synth`, but stops only at left records in one of the states `EVS` |
| `learn.py` | `parse(t)`: split a record tape into `W u^n S` (longest periodic run `u`, period ≤ 6, at least 6 repetitions) |
| `evstep.py` | `evrun(TM, q, tape, evs)`: one event step with `synthev` |
| `orbit.py` | class `Orbit(TM, evs)`: for a key `(q, W, u, S)` learn the rule `n' = a·n + b` per residue class `n mod m` (m from 1 to 96) from synthetic runs with small `n`, then step exactly with big integers |
| `runorb.py` | `TM evs rawfile B tag [timelimit]`: exact orbit of `B` events, writes `orb<tag>.txt` and `rules<tag>.pkl` |
| `horizon.py` | `TM evs tag D NS`: mean probability of HALT within `D` events over `NS` sampled orbit keys, with uniform residues of `n` over the learned rules (a Markov chain on the keys) |
| `coinc.c` | coin model in C: residues of `n` drawn at random at every macro step |

**Method.** At an event (a left record in a chosen state) the tape is `W u^n S` with one long periodic run.
The next event depends on `n` only through `n mod m` and is again of this form with `n' = a·n + b`.
The rule is learned once per key from three synthetic runs per residue class (`n ≈ 300 + 4·(|W|+|S|)`) and checked
for consistency; afterwards the orbit is followed with exact big integers, far beyond direct simulation.
A HALT entry in a learned rule means: HALT in the next event for that residue class.

**Coin model caveat.** The coin model assumes that the residues of `n` are uniformly random. This fails when the
residues are structurally constrained (no. 82); then only the exact orbit is meaningful.
