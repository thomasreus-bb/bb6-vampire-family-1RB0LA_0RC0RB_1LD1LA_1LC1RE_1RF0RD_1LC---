# m70: tools for no. 70 (1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE), also no. 86

Main tools (Python 3 and gcc needed; `lev70` is compiled automatically from `lev70.c`):

| file | content |
|---|---|
| `macro70.py` | on-the-fly macro simulator: rules (x mod 12, stack prefix) -> x' = 3x/2 + c, learned by direct simulation when first needed (cache `rules70.pkl`) |
| `watch70.py` | long run that improves the halting-rate estimate in rounds (default 15 minutes) and judges stationarity; report `watch70_report.txt`, checkpoint `watch70_state.pkl` (a restart continues from it) |
| `check_macro70.py`, `check_msim70.py` | checks of the macro simulator against the direct run and against `mgen/msim.py` |
| `coin70.py`, `inject70.py`, `rate70.py`, `odd70.py` | earlier experiments (coin model, injection tests, stationarity) |

Continue the run on your own computer:

    cd scan/m70
    python3 watch70.py                 # rounds of 15 minutes, runs until stopped (Ctrl-C loses at most the current round)
    python3 watch70.py --minutes 60    # longer rounds
    tail -12 watch70_report.txt        # latest estimate

Start from scratch with `--fresh` (the rule cache is kept). Memory: the stack grows by about 0.56 entries per level
(about 10⁶ levels per 100 MB of RAM); the time per level grows with the number of digits of x (about 0.18 per level).
