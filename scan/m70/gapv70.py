"""gapv70.py - like gap70.py, but the real new block 7 (position 1) is replaced by a block v (3 or 1).
v = 3: counts 'a block 1 appears among the first three blocks'; v = 1: counts HALT.  W Bells, coin parities.
usage: python3 gapv70.py dump70.txt v K W nstates gaps..."""
import sys, random
from fate70 import trial, Short, load
fn, v, K, W, ns = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
gaps = [int(g) for g in sys.argv[6:]]
random.seed(3)
S = [s for s in load(fn, 7) if s[2] == 7][:ns]
for G in gaps:
    c = {'smaller': 0, 'halt': 0, 'no': 0}; n = 0
    for s in S:
        for _ in range(K):
            t = s[:]; t[1] = G; t[2] = v
            try: c[trial(t, v, W)] += 1; n += 1
            except Short: pass
    print('v %d gap %3d: smaller %d, HALT %d of %d (%.3f %% / %.3f %%)' % (v, G, c['smaller'], c['halt'], n,
          100.0*c['smaller']/max(n,1), 100.0*c['halt']/max(n,1))); sys.stdout.flush()
