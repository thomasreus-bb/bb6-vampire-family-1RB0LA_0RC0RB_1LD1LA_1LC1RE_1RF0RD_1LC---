"""gap70.py - P(smaller odd block within W Bells) as a function of the gap in front of the block.
Real states with a new block v at position 1 ([m, G, v, ...]); G is replaced by test values."""
import sys, random
sys.argv_save = sys.argv[:]
from fate70 import trial, Short, load
fn, v, K, W = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
random.seed(2)
S = [s for s in load(fn, v) if s[2] == v][:int(sys.argv[5]) if len(sys.argv) > 5 else None]
for G in (1, 4, 7, 10, 20, 40, 67, 100, 130):
    hit = n = 0
    for s in S:
        for _ in range(K):
            t = s[:]; t[1] = G
            try:
                r = trial(t, v, W)
                n += 1; hit += r == 'smaller'
            except Short: pass
    print('v %d gap %3d: %d of %d (%.3f %%)' % (v, G, hit, n, 100.0*hit/max(n, 1))); sys.stdout.flush()
