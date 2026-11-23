# No. 90: `1RB1LB_1LC1LA_1RD0LB_1RA1RE_1RF0RD_---1RD`

Tools built from the DeepMind acceleration (cryptids repo, BB6 Accelerations README, section 2.2).

| file | purpose |
|---|---|
| `dm90.py` | the map, state (a, L, d, R); `step()` returns None on HALT |
| `check90.py` | compares the map with a direct TM simulation (`python3 check90.py 200000000`) |
| `fast90.py` | run-length encoded stacks, big integers, Bell jumps (`python3 fast90.py 400 20`) |
| `stats90.py` | read-depth statistics per Bell (`python3 stats90.py 100000`, about 30 s) |

Bell rule (4 macro steps): (0, [0^n, 3, 1], 5, [0^c]·R) → (0, [0^(n+5), 3, 1], 5, [0^(c-2)]·R). The counter in L grows by a factor of about 5/2 per Bell. R grows by about 2.1 entries per Bell. The read depth into R was at most 7 over 100,000 Bells, so the machine is probably nonhalting.
