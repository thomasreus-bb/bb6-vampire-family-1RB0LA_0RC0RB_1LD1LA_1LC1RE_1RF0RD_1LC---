# No. 113: `1RB0LC_1LC0RE_1LD1LB_1LA1LD_1RF0RA_---1RE` (Holdout Guide #133)

Same transition table as #581 = `1RB1RD_1RC1RB_1LD0RA_1RA0LE_1LF0LC_---1LE` (bbchallenge id 172044), which halts after about 8.53·10¹³¹ steps (open busycoq PR #76). No. 113 is that table mirrored, with the states renamed (A B C D E F of no. 113 = C D A B E F of #581), started in state C of #581. Checked by simulating both side by side (2·10⁶ steps, identical up to the mirror).

| file | purpose |
|---|---|
| `run113.py` | runs no. 113 with the exact accelerator of the #581 proof (`py/accel.py`, `py/rl.py` of [busy-beaver-explorer](https://github.com/fractal-geometry-explorer/busy-beaver-explorer), folder `holdouts/1RB1RD_1RC1RB_1LD0RA_1RA0LE_1LF0LC_---1LE`, plus `tools/py/bbtools`); edit the two paths at the top. `python3 run113.py 2 SECONDS 2` (start state C of #581, report every factor 100 of visits); `python3 run113.py 0 …` gives the #581 run as a check |
| `run113_log.txt` | the run of 24 Nov 2026: 20 minutes, up to about 10¹²⁵ visits (about 10²⁵¹ steps), no HALT |
