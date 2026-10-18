# Orbit O1: fast simulation with checkpoints

Orbit O1 is the orbit of TM1 (`1RB---_1LC0RB_0LD0LC_1RE1RB_1RD1LF_1LA0LE`), see the main [README](../../README.md) and the TM1 repository.
This directory is self-contained: copy it, compile `bellntt`, and continue the simulation from the last checkpoint.

## How it works
`bellntt` computes the orbit with the Bell map of TM1 (`0^∞ 1^k F> S 0^∞`, k' = 3·⌊k/2⌋ + c, (S', c) from the table `tab.txt` / `tab_names.txt`, the same table as in the TM1 repository).
Bell numbers are those of TM1 (Bell 1: k = 2, S = `11`). In TM2 coordinates (used in `progress.log`) n = ⌊k/2⌋, P = (S without its leading `11`) read backwards.

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
    time 13:01:26
    program bellntt-ckpt-1 (bb6 vampire family)
    orbit O1
    bell 1000001
    S 111
    k_bits 584967
    k_hex 77CD15E1D27682E7...
    time_per_bell 2.5e-06 s (average over Bells 30000000-40000000, run time 25.232 s)
    checksum 6abfcd4e6470c057

- `S` is the word S of TM1 coordinates, `k_hex` the number k in hexadecimal (most significant digit first; decimal would be very slow to compute for numbers with billions of digits).
- `time_per_bell` is the mean computing time per Bell since the previous checkpoint of the run (if that span is shorter than half the interval, since the checkpoint before); it shows how the run time per Bell grows. It is missing in the start checkpoints and in the shipped checkpoint at Bell 1,000,001, which was written by an earlier version. It is not part of the checksum.
- `checksum` is the 64-bit FNV-1a hash of the three lines `bell …`, `S …` and `k_hex …` (each with its newline). A file with a wrong checksum is skipped.
- A first checkpoint can be written by hand with `./bellntt init BELL K S` (for K < 2⁶⁴).

Shipped checkpoints: `bell_5_chkpt.txt` (k = 92, S = `11`, TM1's Bell 5, the start value of `bellntt` in the TM1 repository) and `bell_1000001_chkpt.txt` (reference, 146 kB).

## Checks
- `KCHECK` after Bells 1,000,005 and 10,000,005 agrees with the reference values of `bellntt` in the TM1 repository (`16887177590821663034 584970 11011` and `10592086495055389818 5849632 10001`; there counted as 10⁶ and 10⁷ Bells from Bell 5).
- The values in TM2 coordinates after Bells 10,001, 100,001 and 1,000,001 agree with an independent iteration of the TM2 table (`src/table.py`, 50,000 words): n mod 2⁶⁴ = 7052909479046563730 / 6399555896360640264 / 3717507622098262573, bit length 5,854 / 58,500 / 584,966, P = ε / `1` / `1`.
- Checkpoints, restart and checksum work as tested for O2 (same program).

## Size and run time
k grows by about 0.585 bits per Bell. A checkpoint holds k in hexadecimal, i.e. about 0.146 bytes per Bell: 146 MB at 10⁹ Bells, 1.46 GB at 10¹⁰.
The program keeps several arrays of the size of k in memory (k, the high part, and the product, together about 4 × the size of k at the target).
Run time on 2 cores (measured for TM1 with the same program core): 10⁷ Bells in a few seconds, 10⁹ Bells in about 25 minutes; beyond that the times grow roughly like N^1.5 (10¹⁰ ≈ 12 h, 10¹¹ ≈ 16 days).
Choose INTERVAL so that writing a checkpoint takes little time compared with the run between two checkpoints (e.g. 10⁷ up to 10⁹ Bells, 10⁸ beyond).
