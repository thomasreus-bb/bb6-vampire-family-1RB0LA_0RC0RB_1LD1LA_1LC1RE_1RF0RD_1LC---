# Nos. 78 / 79 / 92 (one transition table): marker structure and perturbation tests (27 Nov 2026)

No. 78 = `1RB1LF_1RC1LD_1LB1LE_1LE0LD_0LA0RE_1RD---`, mirrored `1LB1RF_1LC1RD_1RB1RE_1RE0RD_0RA0LE_1LD---`
(the rare records are then on the left). Nos. 79 and 92 are the same table with other start states.
The scripts were run in `/tmp/an78/` and `/tmp/an/`; paths are hard-coded.

| file | purpose |
|---|---|
| `exc.c` | `exc TM N`: every record; for right records also the depth of the last excursion (how far left the head went) |
| `pass78.c` | `pass78 TM q maxsteps`: run from a tape on stdin to the next left record in state E; prints the turning points below 400 cells |
| `var78.py` | perturbation test: add/remove markers in the tape of a left record, run to the next left record |
| `chain78.py` | chains of perturbed left-record cycles (perturb, run, perturb the result, ...) up to 25,000 cells |
| `chain78_out.txt` | output of `chain78.py` (40 chains from the E records with 532 and 1,020 cells) |

## Structure (mirrored no. 78, direct run to 3·10⁹ steps)

- Left records are rare (32 in 2.45·10⁹ steps), right records frequent. Read as tokens a = `10`, b = `100`,
  C = `110`, D = `1000`, the tape is a sea of `ab ab ab ...` with sparse defects.
- **Markers:** every left record leaves a D marker at the old right end. The D positions are the earlier tape
  lengths (33, 42, 67, 120, 219, 412, 1,545, 3,066, 12,159 tokens at the last left record): a record of the
  machine's own history, like digits.
- **Prefix:** the first ~25 tokens alternate between two fixed forms (`abaCbaCbababababababaCb…` and
  `DabaCbababaCbabab…`) from one left record to the next.
- **Two-sided Bell:** the head bounces between the right end and a turning point. Per bounce the right end moves
  5 cells right and the turning point 5 cells left (the depth grows by 10). At a marker the turning point jumps
  9 cells instead of 5, so each marker shifts the phase by one cell (mod 5).
- **Pass end:** when the turning point reaches the prefix, there are two outcomes: a left record (the prefix
  flips its form), or a reset: the turning point jumps back to the right end without a left record. Each pass
  doubles the tape, so the length grows by ×2 or ×4 between left records (1,020 → 3,860 → 7,668 → 30,408 → 60,756).
  Which outcome happens depends on the phase of arrival, i.e. on the tape length mod 5 and the number of markers:
  pseudo-random "chaotic digits".
- **Nos. 79 and 92** show the same prefix forms and the same marker sea (with other marker positions; no. 92 also
  has an `aa` defect). They share the macro dynamics of no. 78.

## Perturbation tests (no. 78)

- `var78.py`: 60 variants of the left record with 1,020 cells (1–3 extra markers): all reach the next left
  record, no HALT (new lengths between 3,000 and 21,000 cells, i.e. 1 to 4 passes).
- `chain78.py`: 40 chains, 116 left-record cycles with random marker perturbations before each cycle, about
  430 pass ends: **0 HALT**. The pass ends fall into a handful of recurring patterns of turning points near the
  left end. 5 chains stopped at the step limit (2·10¹⁰ steps at 10⁴–2.4·10⁴ cells):
  artificial marker configurations that change the dynamics; such configurations are not known to occur in the
  real runs.

## Assessment

A lottery structure (outcome of each pass decided by a pseudo-random phase), but HALT is not one of the observed
outcomes: no pass end in the direct runs or in the perturbed chains comes close to halting. A Markov estimate of
the HALT probability is not possible yet: there is no halting branch to give a rate. **No basis for HALT > 90 %;
probably nonhalting.** A proof would need the finite list of pass-end cases (prefix form × arrival phase) and the
marker rule as inductive statements.
