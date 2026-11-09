# Exact level maps (nos. 105 and 73)

`gcc -O2 -o gmap gmap.c; gcc -O2 -o gmap2 gmap2.c; gcc -O2 -o ev ev.c; gcc -O2 -o evb evb.c` in this folder.

- `gmap.c` / `gmap2.c`: run one level from a level configuration (head left of all nonzero cells, `PREFIX 1^n W` or `PREFIX UNIT^n W`) to the next one, or to HALT.
- `glev.py`, `glev2.py`: exact level iteration. For n = m q + r the next level is a q + e, with (e, W') depending only on (r, W) once q is large compared with W; the table is computed by direct simulation at two values of q that must agree.
- `check.py`: level iteration against direct simulation (`ev`).
- `run105.py`, `run73b.py`: long runs with tail statistics; `tab105.pkl`, `../m73/tab73.pkl`: the tables.
- `rhalt*.py`, `inv*.py`, `scan*.py`, `hmap.py`: random and systematic searches for halting levels.
- `try.sh`, `certs.txt`, `r105.txt`: busycoq's verified CTL deciders (CTL62) with 84 parameter sets on no. 105.

No. 73 uses the mirrored machine (state D, unit `110`).
