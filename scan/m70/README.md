# m70: tools for no. 70 (1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE), also no. 86

Main tools (Python 3 and gcc needed; `lev70` is compiled automatically from `lev70.c`):

| file | content |
|---|---|
| `macro70.py` | on-the-fly macro simulator: rules (x mod 12, stack prefix) -> x' = 3x/2 + c, learned by direct simulation when first needed (cache `rules70.pkl`) |
| `sim70.c` | **fast C version** of the real macro run (no library needed): `gcc -O2 -o sim70 sim70.c`, then `./sim70`; checkpoint `sim70.ck` (Ctrl-C saves), progress every 60 s, every block 7, 5, 3, 1 near the front is logged in `events70.txt`. Same rules and results as the Python run (check values at Bell 4,663,800 identical); about 1 million Bells/s at the start, 57,000 Bells/s at 10⁸ Bells |
| `watch70.py` | long run that improves the halting-rate estimate in rounds (default 15 minutes) and judges stationarity; report `watch70_report.txt`, checkpoint `watch70_state.pkl` (a restart continues from it) |
| `check_macro70.py`, `check_msim70.py` | checks of the macro simulator against the direct run and against `mgen/msim.py` |
| `coin70.py`, `inject70.py`, `rate70.py`, `odd70.py` | earlier experiments (coin model, injection tests, stationarity) |

Continue the run on your own computer:

    cd scan/m70
    python3 watch70.py                 # rounds of 15 minutes, runs until stopped (Ctrl-C loses at most the current round)
    python3 watch70.py --minutes 60    # longer rounds
    tail -12 watch70_report.txt        # latest estimate

Start from scratch with `--fresh` (the rule cache is kept). Memory: the stack grows by about 0.56 entries per Bell
(about 10⁶ Bells per 100 MB of RAM); the time per Bell grows with the number of digits of x (about 0.18 per Bell).

Fast run in C (recommended):

    gcc -O2 -o sim70 sim70.c
    ./sim70                  # Ctrl-C: checkpoint is saved; ./sim70 again continues
    ./sim70 -n 4663800       # test: must print bits 2728153, x mod 2^64 = 0x58106550ccb57c0e, stack 2616485, hash 884327361506333381

Memory: about 0.56 stack entries per Bell (4 bytes each) plus x (0.585 bits per Bell): about 260 MB at 10⁸ Bells,
2.6 GB at 10⁹ Bells. The checkpoint file has the same size.
