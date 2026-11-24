# No. 86 against no. 70

| file | purpose |
|---|---|
| `rec86.c` | direct simulation of both machines; at every new leftmost cell (state A for no. 70, state B for no. 86) the tapes are compared as run-length lists, all runs except the right ends (last 4 runs of no. 70, last 2 of no. 86). `gcc -O2 -o rec86 rec86.c && ./rec86 3000000000 200 4 2` |
| `sim70bottom.c` | `sim70dz.c` with a monitor of how close the reading of the stack comes to the stack bottom (where the two machines differ). Compile like `sim70dz.c`. |
| `bottom.log` | its output for 3·10⁸ Bells |
| `cut86.c` | end test: aligned real configurations with the stack cut down to KEEP runs, both machines run on and are compared at every record (`./cut86 3000 4 300 2000000000`) |
