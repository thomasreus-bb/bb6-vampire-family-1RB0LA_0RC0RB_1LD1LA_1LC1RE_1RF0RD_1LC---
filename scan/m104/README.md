# No. 104: `1RB1RE_1LC1LB_1LE0LD_1LE1LC_0RF1RA_---1RA`

Tools built from the DeepMind acceleration (cryptids repo, BB6 Accelerations README, section 2.5).

| file | purpose |
|---|---|
| `dm104.py` | the map, state (d, R); `step()` returns None on HALT |
| `check104.py` | compares the map with a direct TM simulation (`python3 check104.py 50000000`) |
| `run104.py` | plain long run of the map (slow) |
| `sim104.c` | fast C version: 64-bit values, run-length encoded stack, Bell jumps; about 100 Bells before overflow. `gcc -O2 -o sim104 sim104.c && BELLS=1 ./sim104 1000000000000000000 1000000000000000000` |
| `fast104.py` | Bell-level simulator with big integers (`python3 fast104.py 3000 500`) |
| `stats104.py` | read-depth statistics per Bell (`python3 stats104.py 100000`, about 7 s) |

Bell rule: (d odd, [3, 0^c]·R) → (d+6, [3, 0^(c-2)]·R). Per Bell, d → (3d+k)/2. The stack grows by about 1.13 entries per Bell. The read depth below the previous Bell's stack length was at most 13 over 100,000 Bells, so the machine is probably nonhalting.
