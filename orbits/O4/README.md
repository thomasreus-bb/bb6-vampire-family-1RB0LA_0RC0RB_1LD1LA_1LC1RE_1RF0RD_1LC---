# Orbit O4: fast simulation with checkpoints

Orbit O4 is the orbit of TM2b (`1RB---_0RC0RB_1LD1LE_1LC1RF_1RB0LE_1RA0RD`); TM2b' runs on it as well (see the main [README](../../README.md)).
This directory is self-contained: copy it, compile `bellntt`, and continue the simulation from the last checkpoint.

## How it works
`bellntt` computes the orbit with the Bell map in TM1 coordinates (`0^∞ 1^k F> S 0^∞`, k' = 3·⌊k/2⌋ + c, (S', c) from the table `tab.txt` / `tab_names.txt`, the same table as in the TM1 repository).
Unlike O1–O3, no machine of the family runs on O4 in TM1 form. The start value was therefore converted from TM2 coordinates: k = 2n, S = `11` + (P read backwards); the checks below show that the TM1 table then reproduces the orbit.
Bell numbers are those of TM2b (Bell 1: TM2b n = 3, P = ε, i.e. TM2 coordinates n = 4, P = ε).
In TM2 coordinates (used in `progress.log`) n = ⌊k/2⌋, P = (S without its leading `11`) read backwards; TM2b's own n is one smaller.

The method is that of `bellntt` in the TM1 repository (blocks of Bells, own NTT multiplication, no GMP); new are the checkpoints, the start from the last checkpoint and the target Bell.

## Usage

    gcc -O3 -march=native -fopenmp -o bellntt bellntt.c -lm     # without -fopenmp: one core
    ./bellntt [-t TARGET] [-i INTERVAL] [-b B]

- `-t TARGET`: Bell number at which the run stops; a checkpoint is written there. **Without `-t` the run goes on until HALT or until it is interrupted (Ctrl-C).**
- `-i INTERVAL`: a checkpoint is written at every Bell number divisible by INTERVAL (default 10,000,000).
- `-b B`: fixed block size in Bells. Without `-b` the block size grows automatically with the Bell number (B = 38·√Bell, at least 40,000); only the speed depends on it.
- The older form `./bellntt TARGET [INTERVAL [B]]` still works.

The run starts from the checkpoint with the highest Bell number in `checkpoints/` that can be read (correct checksum).
During the run each new intermediate checkpoint replaces the previous one, so the file name shows the progress; the start checkpoint, the target checkpoint and always the newest checkpoint are kept.
A run can be stopped at any time (Ctrl-C) and continues from its newest checkpoint when started again.
Every checkpoint also adds a line to `progress.log` (date, Bell, run time, `KCHECK`, and the values in TM2 coordinates).

Examples:

    ./bellntt                          # from the newest checkpoint on, until HALT or Ctrl-C, checkpoint every 10^7 Bells
    ./bellntt -t 1000000000            # up to Bell 10^9
    ./bellntt -i 100000000             # endless, checkpoint every 10^8 Bells

If the orbit reaches a HALT entry of the table, the program says so, writes `checkpoints/HALT_bell_<N>.txt` and stops. If it reaches a word that is not in the table, it writes `checkpoints/UNKNOWN_bell_<N>.txt`.

## Checkpoint files
**Note (21 Oct 2026):** `bellntt` and `bellnttp` versions from before 21 Oct 2026 wrote **unreadable checkpoints once k had more than 8.6·10⁹ bits** (Bell above about 1.47·10¹⁰), because `fprintf` cannot write strings longer than 2³¹ − 1 characters. The runs themselves and their `progress.log` values are correct; only such checkpoints cannot be used. Fixed in the current versions (and `belldc` was never affected).

A checkpoint is a text file `checkpoints/bell_<N>_chkpt.txt` for one Bell N:

    # bellntt checkpoint
    date 2026-10-18
    time 12:13:26
    program bellntt-ckpt-1 (bb6 vampire family)
    orbit O4
    bell 1000001
    S 111
    k_bits 584968
    k_hex 8B0F099CB3951572...
    time_per_bell 2.5e-06 s (average over Bells 30000000-40000000, run time 25.232 s)
    checksum 3fb15535371a8401

- `S` is the word S of TM1 coordinates, `k_hex` the number k in hexadecimal (most significant digit first; decimal would be very slow to compute for numbers with billions of digits).
- `time_per_bell` is the mean computing time per Bell since the previous checkpoint of the run (if that span is shorter than half the interval, since the checkpoint before); it shows how the run time per Bell grows. It is missing in the start checkpoints and in the shipped checkpoint at Bell 1,000,001, which was written by an earlier version. It is not part of the checksum.
- `checksum` is the 64-bit FNV-1a hash of the three lines `bell …`, `S …` and `k_hex …` (each with its newline). A file with a wrong checksum is skipped.
- A first checkpoint can be written by hand with `./bellntt init BELL K S` (for K < 2⁶⁴).

Shipped checkpoints: `bell_5_chkpt.txt` (k = 110, S = `111`, converted from TM2b's Bell 5: TM2 coordinates n = 55, P = `1`) and `bell_1000001_chkpt.txt` (reference, 146 kB).

## Checks
- The values in TM2 coordinates after Bells 10,001, 100,001 and 1,000,001 agree with an independent iteration of the TM2 table (`src/table.py`, 50,000 words) from TM2b's first Bell: n mod 2⁶⁴ = 17089104364164062285 / 3983368811517645662 / 17957952829979503584, bit length 5,854 / 58,500 / 584,967, P = `101` / `1` / `1`.
- The TM2 table iteration itself reproduces the first 14 directly simulated Bells of TM2b (`src/cyc.c`).
- Checkpoints, restart and checksum work as tested for O2 (same program).

## Size and run time
k grows by about 0.585 bits per Bell. A checkpoint holds k in hexadecimal, i.e. about 0.146 bytes per Bell: 146 MB at 10⁹ Bells, 1.46 GB at 10¹⁰.
The program keeps several arrays of the size of k in memory (k, the high part, and the product, together about 4 × the size of k at the target).
Run time on 2 cores: 10⁸ Bells in about 1 minute (measured with this program), 10⁹ Bells in about 25 minutes (measured for TM1 with the same program core); beyond that the times grow roughly like N^1.5 (10¹⁰ ≈ 12 h, 10¹¹ ≈ 16 days).
Choose INTERVAL so that writing a checkpoint takes little time compared with the run between two checkpoints (e.g. 10⁷ up to 10⁹ Bells, 10⁸ beyond).

## bellnttp: horizon pruning and distance to HALT
`bellnttp.c` is `bellntt.c` with two additions (details in the main [README](../../README.md#horizon-pruning-and-bellnttp)):

    gcc -O3 -march=native -fopenmp -o bellnttp bellnttp.c -lm
    ./bellnttp -t 20000000000 -p -i 100000000      # pruned run towards Bell 2·10¹⁰

- `-p` (only together with `-t T`): keeps only k mod 2^((T − Bell) + 128). From Bell ≈ 0.63·T on, the numbers shrink towards T; memory and time go down. KCHECK and S stay comparable with full runs, the bit length is the pruned one (the log line says `pruned to T`). Pruned checkpoints are named `bell_<N>_pchkpt.txt`; such a run cannot be continued beyond T. `bellntt` ignores pruned checkpoints.
- Without `-p`, `bellnttp` works exactly like `bellntt` and continues from the same checkpoints, so switching from `bellntt` to `bellnttp` is possible at any time (stop `bellntt` with Ctrl-C, start `bellnttp`).
- Every log line ends with `d <d(S)> D <D> (Bell <N>)`: d(S) is the smallest number of Bells from the current word S to a HALT entry of the table, D the smallest d reached so far (and where). D is also written into the checkpoints.

## belldc: divide and conquer with GMP (about 10 times faster)
`belldc.c` computes the same orbit with a recursive (divide and conquer) block method and GMP multiplication; details and measurements in the main [README](../../README.md#belldc-divide-and-conquer-with-gmp).

    sudo apt install -y libgmp-dev                 # once
    gcc -O3 -march=native -o belldc belldc.c -lgmp
    ./belldc -t 20000000000 -i 1000000000          # full run to Bell 2·10¹⁰, checkpoint every 10⁹ Bells
    ./belldc -t 100000000000 -p -i 5000000000      # pruned run towards 10¹¹
    ./belldc -t 100000000000 -p -m -i 5000000000   # the same with less memory (about 1.6 × k instead of 3.6 × k, a little slower)

- Same options as `bellnttp` (`-t`, `-p`, `-i`, `-b`) plus `-m`; default checkpoint interval 10⁹ Bells.
- Same checkpoint files and log lines (KCHECK, d and D) as `bellntt` / `bellnttp`: switching between the programs is possible at any time (Ctrl-C, start the other one).
- One core (GMP). The largest checkpoint files can be several GB; keep space for two of them.
- **Pruned runs and later continuation (22 Oct 2026).** Pruning only starts cutting bits of k at about Bell TARGET/1.585 (about 6.3·10¹⁰ for TARGET = 10¹¹). Up to there, `belldc -p` now writes normal, exact `chkpt` files and **keeps the last exact one** (the others are rotated as before), e.g. `bell_60000000000_chkpt.txt` for `-t 100000000000 -p -i 5000000000`. A later run to a higher target can start from it instead of from the beginning (`./belldc -t 200000000000 -p …`). Old `pchkpt` files written by earlier versions before pruning started (k far shorter than (TARGET − Bell) + 128 bits, e.g. the multi-GB ones) are recognised as exact when read and used as full checkpoints. The small `pchkpt` files near the target (a few hundred bytes) are only k mod 2^((TARGET − Bell)+128) and cannot be continued beyond TARGET.
