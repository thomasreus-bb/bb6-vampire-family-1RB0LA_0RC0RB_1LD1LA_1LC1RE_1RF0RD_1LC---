"""fate70.py - what happens to the small odd blocks that the REAL run of no. 70 creates?
Reads dump70.txt (front of the stack before/after every Bell in which a block 7 or 5 appeared
among the first three stack blocks, from sim70ev) and continues each real state with coin-flip
parities (rules from macro70.py), W Bells, K repetitions.  Counts: a smaller odd block appears among
the first three stack blocks.  For comparison the same test with an injected block (watch70 style).
usage: python3 fate70.py dump70.txt v K W"""
import sys, os, random
M70 = os.path.dirname(os.path.abspath(__file__))
os.chdir(M70); sys.path.insert(0, M70)
import pickle, macro70
from macro70 import rule, RULES
RULES.update(pickle.load(open('rules70.pkl', 'rb')))
class Short(Exception): pass
def front(R, k): return R[:-k-1:-1] if len(R) > k else R[::-1]
def fastrule(x, R):
    k = 18
    while True:
        P = front(R, k); whole = len(P) == len(R)
        r = rule(x, P)
        if r[0] == 'HALT': return r
        if r[4] and not whole: k *= 4; continue
        if r[4]: raise Short()          # would need more than the dumped front
        return r
def apply(x, R, r):
    if r[0] == 'HALT': return None
    _, lp, fits, sf, inf = r
    vals = [int(bb) for aa, bb in fits[1:]]
    del R[len(R)-lp:]
    out = [vals[0]]; i = 1
    while i+1 < len(vals):
        g, bb = vals[i], vals[i+1]
        if g == 0: out[-1] += bb
        else: out += [g, bb]
        i += 2
    if i < len(vals):
        g = vals[i]
        if g == 0 and R: out[-1] += R.pop()
        else: out.append(g)
    R.extend(reversed(out)); return 1
def first3(R): return [b for b in front(R, 8)[2::2]]
def coin(R):
    xf = 60 + random.choice((0, 6)) + 12*random.randint(0, 63)
    return apply(xf, R, fastrule(xf, R))
def trial(front_list, v, W):
    R = front_list[::-1]
    for _ in range(W):
        if coin(R) is None: return 'halt'
        if any(b % 2 and b < v for b in first3(R)): return 'smaller'
        if v not in first3(R): pass
    return 'no'
def load(fn, v):
    out = []
    lines = open(fn).read().split('\n')
    for l in lines:
        if l.startswith('A ') and int(l.split()[2]) == v:
            out.append(list(map(int, l.split('|')[1].split())))
    return out
if __name__ == '__main__':
    fn, v, K, W = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    random.seed(1)
    states = load(fn, v)
    tot = {'smaller': 0, 'no': 0, 'halt': 0, 'short': 0}; per = []
    for s in states:
        c = {'smaller': 0, 'no': 0, 'halt': 0, 'short': 0}
        for _ in range(K):
            try: c[trial(s, v, W)] += 1
            except Short: c['short'] += 1
        per.append(c['smaller']); 
        for k in c: tot[k] += c[k]
    n = tot['smaller'] + tot['no'] + tot['halt']
    print('real states with a new block %d: %d; runs %d; smaller odd block within %d Bells: %d (%.3f %%); short %d'
          % (v, len(states), n, W, tot['smaller'], 100.0*tot['smaller']/max(n, 1), tot['short']))
    print('per state (of %d):' % K, per)
    # injection control: same real states, the first odd block v replaced ... use the B-states' stacks of other events
    inj = {'smaller': 0, 'no': 0}; ni = 0
    for s in states:
        for _ in range(K):
            t = s[:]; pos = random.randint(1, 3)
            if len(t) <= 2*pos: continue
            # remove the real small block first (make it 9, like most fronts), then inject v at pos
            for j in (2, 4, 6):
                if t[j] % 2 and t[j] < 9: t[j] = 9
            t[2*pos] = v
            try:
                r = trial(t, v, W)
                if r != 'halt': inj[r] += 1; ni += 1
            except Short: pass
    print('injection control (v at a random position 1..3 of the same stacks): %d of %d (%.3f %%)'
          % (inj['smaller'], ni, 100.0*inj['smaller']/max(ni, 1)))
