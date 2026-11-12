# No. 41: exact macro step and halting Bell values (12 Nov 2026)

- `m41.py`: the six macro configurations (P1, P2, P3, Q, A, Bell) and one macro step by direct simulation
  (the first later configuration of one of these forms).
- `tab.py 14`: table of the macro step for all counters ≤ 14 (`tab14.pkl`).
- `macro.py`: macro step for all counter values (table plus affine continuation), with jumps over the loops;
  `cycle(n)` gives the next Bell or `HALT`.
- `inv2.py 24 60 40`: closure of the residue classes modulo 24 from the Bell class n ≡ 4 (mod 8).
- `bell.c`: direct simulation from the Bell configuration `1 (10)^n [0]`, state A (`./bell 62156 400000000000`).
