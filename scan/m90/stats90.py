"""stats90.py - Bell statistics for candidate 90 (uses fast90.M90).
Halting needs the right stack R to be used up completely.  Per Bell we
record how far R shrinks below its length at the previous Bell (eat
depth, measured after each macro step) and how often R is empty.
Usage: python3 stats90.py [bells]"""
import sys, collections, time
from fast90 import M90
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
M = M90(); eats = collections.Counter(); per = collections.Counter()
last = None; low = None; empty = 0; nst = 0; t = time.time()
while M.bells < N and not M.halted:
    if M.bell_jump():
        if last is not None: eats[last - low] += 1; per[nst] += 1
        last = low = M.R.n; nst = 0
        if M.bells % 20000 == 0:
            print('bell', M.bells, '|R|', M.R.n, 'R runs', len(M.R.v), 'log2|L| %d' % M.L.n.bit_length(),
                  'max eat', max(eats), '%.0fs' % (time.time()-t)); sys.stdout.flush()
        continue
    M.step(); nst += 1
    if M.R.n == 0: empty += 1
    if low is not None: low = min(low, M.R.n)
if M.halted: print('HALT', M.steps, M.bells)
print('R empty after a macro step:', empty, 'times')
print('eat depth distribution', sorted(eats.items()))
print('macro steps between Bells', sorted(per.items())[:30], '... max', max(per))
