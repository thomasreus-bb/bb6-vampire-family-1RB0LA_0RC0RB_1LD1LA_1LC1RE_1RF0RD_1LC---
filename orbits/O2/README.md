# Orbit O2: fast simulation with checkpoints

Orbit O2 is the orbit of TM2 (`1RB0LA_0RC0RB_1LD1LA_1LC1RE_1RF0RD_1LC---`); TM1-F and TM2' run on it as well (see the main [README](../../README.md)).
This directory is self-contained: copy it, compile `bellntt`, and continue the simulation from the last checkpoint.

## How it works
`bellntt` computes the orbit with the Bell map in TM1 coordinates (`0^∞ 1^k F> S 0^∞`, k' = 3·⌊k/2⌋ + c, (S', c) from the table `tab.txt` / `tab_names.txt`, the same table as in the TM1 repository).
This is possible because O2 is also the orbit of TM1-F, i.e. of TM1 started in state F.
Bell numbers are counted as for TM2: TM2's Bell N is TM1-F's Bell N + 1, and in TM2 coordinates n = ⌊k/2⌋, P = (S without its leading `11`) read backwards.

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
    time 11:54:06
    program bellntt-ckpt-1 (bb6 vampire family)
    orbit O2
    bell 1000001
    S 11
    k_bits 584968
    k_hex 85746D0B325A9352...
    checksum 9c8e8bb901d620c9

- `S` is the word S of TM1 coordinates, `k_hex` the number k in hexadecimal (most significant digit first; decimal would be very slow to compute for numbers with billions of digits).
- `checksum` is the 64-bit FNV-1a hash of the three lines `bell …`, `S …` and `k_hex …` (each with its newline). A file with a wrong checksum is skipped.
- A first checkpoint can be written by hand with `./bellntt init BELL K S` (for K < 2⁶⁴).

Shipped checkpoints: `bell_5_chkpt.txt` (k = 104, S = `111`, the start of the orbit as computed here; TM2's Bell 5: n = 52, P = `1`) and `bell_1000001_chkpt.txt` (reference, 146 kB).

## Checks
- The values in TM2 coordinates after Bells 10,001, 100,001 and 1,000,001 agree with the fingerprints in [TM2.md](../../TM2.md), which were computed with TM2's own table (49,993 words): n mod 2⁶⁴ = 10344533065338383136 / 11927179264807263660 / 16065736760597740477, bit length 5,854 / 58,500 / 584,967, P = ε / `11` / ε. So two independently built tables give the same orbit.
- A run from Bell 1,000,001 to 20,000,001 in one go and the same run interrupted and continued give the same checkpoint (KCHECK 16507680289743261104 11699255 11).
- A checkpoint with a changed Bell number is rejected because of its checksum.

## Size and run time
k grows by about 0.585 bits per Bell. A checkpoint holds k in hexadecimal, i.e. about 0.146 bytes per Bell: 146 MB at 10⁹ Bells, 1.46 GB at 10¹⁰.
The program keeps several arrays of the size of k in memory (k, the high part, and the product, together about 4 × the size of k at the target).
Run time on 2 cores (measured for TM1 with the same program core): 10⁷ Bells in a few seconds, 10⁹ Bells in about 25 minutes; beyond that the times grow roughly like N^1.5 (10¹⁰ ≈ 12 h, 10¹¹ ≈ 16 days).
Choose INTERVAL so that writing a checkpoint takes little time compared with the run between two checkpoints (e.g. 10⁷ up to 10⁹ Bells, 10⁸ beyond).
