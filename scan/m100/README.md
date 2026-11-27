# No. 100 (`1RB1RD_1LC0RD_1RF1RB_1LE0RA_0LB0LE_---0RC`): Collatz map from the DeepMind reduction (27 Nov 2026)

Source of the map: DeepMind cryptids repository, `BusyBeaver/BB6/Accelerations/FixedArityReduction/
M_1RB1RD_1LC0RD_1RF1RB_1LE0RA_0LB0LE_HHH0RC.lean` (Lean, kernel-verified `HasCollatzReduction`).
Configurations C(k, a, b) = 0^∞ (10101)^k C> 0 1 0 1^a 0 1^b 0^∞, start C(0, 2, 0) after 10 steps.

| file | purpose |
|---|---|
| `col100.py` | the map `step(k, a, b)` and `drainB(b, w)`, transcribed from the Lean file |
| `chk.py` | check against the direct TM run: the first 40 C-configurations agree exactly with the map |
| `fast100.py` | accelerated map (even a with b = 0 counts down in one jump; odd a ≥ 7 drops by 6 per step in one jump) |

## HALT channels of the map

- C(k, 0, b); C(k, 1, 0); C(k, 1, 1); C(k, 1, 7) (via drainB(5)); C(k, 7, 0) (→ C(k+1, 1, 1));
- drainB(b, w) with b ≡ 5 (mod 6) recurses with b → (b − 11)/6 and halts if it ends exactly at 5. For a large
  random b this needs about log₆ b digits equal to 5 in a row: probability about 1/b.

So every HALT channel needs a or b to be a **small exact value**, or an event with probability about 1/b.

## Run

- `fast100.py` for 60 s: 768,927 macro steps, k and b reach about 73,700 digits. No HALT.
- After the first 2,000 macro steps every value that enters a HALT channel has **at least 195 digits**
  (a = 1, 3, 5: b ≥ 10^195; odd a with b = 0: a ≥ 10^196; even-a drains: b ≥ 10^200). Small values never recur:
  even a counts down to 2 with b = 0, odd a counts down to 1, 3 or 5 with b growing by the same number of steps.

## Markov-type estimate

Under the random-residue model the HALT probability of one macro step is at most about 1/b with b ≥ 10^195 after
2,000 steps, and the sizes keep growing. The sum over all future steps is below about 10^-190.
**P(HALT) is practically 0: probably nonhalting.** It is a Collatz-like map, but without a realistic halting
channel (unlike Antihydra-type maps, where halting is a random-walk event of probability bounded away from 0).
