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

    gcc -O3 -march=native -fopenmp -o bellntt bellntt.c     # without -fopenmp: one core
    ./bellntt TARGET [INTERVAL [B]]

- `TARGET`: Bell number at which the run stops; a checkpoint is written there.
- `INTERVAL`: a checkpoint is written at every Bell number divisible by INTERVAL (default 10,000,000).
- `B`: block size in Bells (default 2,000,000; only the speed depends on it, see the TM1 repository for good values).

The run starts from the checkpoint with the highest Bell number in `checkpoints/` that can be read (correct checksum).
During the run each new intermediate checkpoint replaces the previous one, so the file name shows the progress; the start checkpoint and the target checkpoint are kept.
A run can be stopped at any time (Ctrl-C) and continues from its last checkpoint when started again.
Every checkpoint also adds a line to `progress.log` (date, Bell, run time, `KCHECK`, and the values in TM2 coordinates).

Example: from the shipped checkpoint at Bell 1,000,001 to Bell 10⁹ with a checkpoint every 10⁷ Bells:

    ./bellntt 1000000000 10000000

If the orbit reaches a HALT entry of the table, the program says so, writes `checkpoints/HALT_bell_<N>.txt` and stops. If it reaches a word that is not in the table, it writes `checkpoints/UNKNOWN_bell_<N>.txt`.

## Checkpoint files
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
Run time on 2 cores (measured for TM1 with the same program core): 10⁷ Bells in a few seconds, 10⁹ Bells in about 25 minutes; beyond that the times grow roughly like N^1.5 (10¹⁰ ≈ 12 h, 10¹¹ ≈ 16 days).
Choose INTERVAL so that writing a checkpoint takes little time compared with the run between two checkpoints (e.g. 10⁷ up to 10⁹ Bells, 10⁸ beyond).
