# Generic tools for the accelerated simulation of Bell-like machines

| file | content |
|---|---|
| `msim.py` | accelerated simulator (runs of BS-cell blocks, chain steps, loop skipping); machine from `TM`, block size from `BS48` |
| `one.py` | one machine for a fixed wall time (`TM=... BS48=40 python3 one.py 45`) |
| `phc.py`, `ph_desc.py` | every time the head is at the left end of the stored tape: print step, state and the tape in compressed form (`[u]^k` = a long run of the unit u); `MIRROR=1` mirrors the machine, `FILTER` selects events |
| `ph.py` | the same at every left record (cell level at the left edge; slow when the left edge itself is the growing part) |
| `rl.py`, `build.py` | parse a description into runs of cells and build a simulator state from it (start from any phase) |
| `hitgen.py`, `chkgen.py` | start from real events with randomly changed long runs, count HALTs; check that an unchanged restart reproduces the real run |
| `famgen.py`, `bsim.c` | the same with direct cell-by-cell simulation (`gcc -O2 -o bsim bsim.c`, run from the folder that holds `bsim`) |

The loop skipping is a heuristic (see `scan/m48`); a result is a measurement, not a proof.
