"""Closure of the abstract Bell map of no. 83 with EXACT symbolic Bell steps (symbell.py).

Abstract state (r, P): r = gap in front of S (1, 2, 3); P = explicit runs of S (block, gap, ..., block), each an
exact int <= SMALL or ('B', c) = any value > SMALL with value = c (mod MOD); after P comes an arbitrary tail T of
(gap, block) pairs with gap in LTG and block in LTB.  N is symbolic: N = 4n + c0, c0 in {101, 103}.
A transition is computed exactly for all values in the classes (fresh variables); outputs are abstracted again.
"""
import sys, json, itertools
sys.path.insert(0, '/tmp/an83')
from sym import Lin, L, Halt, Touched, NeedSplit, REST
import symbell
from collections import deque, Counter

SMALL = int(sys.argv[1]) if len(sys.argv) > 1 else 12
MOD = int(sys.argv[2]) if len(sys.argv) > 2 else 4
LIMIT = int(sys.argv[3]) if len(sys.argv) > 3 else 100000

def base(c):
    v = SMALL + 1
    while v % MOD != c: v += 1
    return v
def B(c): return ('B', c)
LT_GAPS = list(range(4, SMALL + 1, 2)) + [B(c) for c in range(MOD) if c % 2 == 0]   # tail gaps even >= 4
UNITS = [(6,), (12,), (6, 2, 6)]   # tail units: 1^6, 1^12, 1^6 0^2 1^6
LT_BLOCKS = [6, 12]   # deep blocks of the real orbit are only 6 and 12
FRONT_BLOCKS = list(range(6, SMALL + 1, 2)) + [B(c) for c in range(MOD) if c % 2 == 0]
LTG, LTB = set(LT_GAPS), set(LT_BLOCKS)

class Ambig(Exception): pass

def absval(e, allowed_vars):
    if any(k not in allowed_vars for k in e.v): raise ValueError(('foreign var', e))
    if not e.v:
        return e.c if e.c <= SMALL else B(e.c % MOD)
    if any(x % MOD for x in e.v.values()): raise ValueError(('coef', e))
    if e.c > SMALL: return B(e.c % MOD)
    raise Ambig(e)

def run_one(r, vals, c0):
    """vals: list of Lin (inputs). returns (M, r2, out) or raises."""
    return symbell.symbell(L(c0, n=4), r, vals)

def trans_concrete(r, vals, varnames, depth=0):
    """returns set of abstract successor states, or raises Halt/Touched/... ; handles Ambig by splitting."""
    succ = set()
    for c0 in (101, 103):
        try:
            M, r2, out = run_one(r, vals, c0)
        except NeedSplit as ns:
            w, e = ns.args[0]
            vs = [k for k in sorted(e.v) if k in varnames]
            if not vs or depth > 10: raise
            succ |= split(r, vals, varnames, vs[0], depth)
            continue
        N = L(c0, n=4)
        dM = M - N
        if not dM.nonneg() or dM.c <= 0 or dM.v.get('n', 0) < 0: raise ValueError(('M<=N', M))
        if M.c % 2 == 0 or any(x % 2 for x in M.v.values()): raise ValueError(('M even', M))
        if M.v.get('n', 0) < 4: raise ValueError(('M coef', M))
        if not out or out[0][0] != '1' or len(out) % 2 == 0:
            raise Touched()    # output ends with a gap next to T (or empty): T's first gap is involved
        P2 = []
        try:
            for w, e in out: P2.append(absval(e, varnames))
        except Ambig as a:
            e = a.args[0]
            v = sorted(e.v)[0]
            if depth > 10: raise ValueError(('deep ambig', e))
            succ |= split(r, vals, varnames, v, depth)
            continue
        while True:
            if len(P2) > 1 and P2[-2] in LTG and P2[-1] in (6, 12) and not (len(P2) > 3 and P2[-3] == 2):
                P2 = P2[:-2]; continue
            if len(P2) > 3 and P2[-4] in LTG and tuple(P2[-3:]) == (6, 2, 6):
                P2 = P2[:-4]; continue
            break
        succ.add((r2, tuple(P2)))
    return succ

def split(r, vals, varnames, v, depth):
    """v = 0  or  v = v' + 1"""
    res = set()
    for sub in (0, 1):
        vals2 = []
        for x in vals:
            if v in x.v:
                k = x.v[v]
                rest = Lin(x.c, {a: b for a, b in x.v.items() if a != v})
                vals2.append(rest + Lin(k, {v: k}) if sub == 1 else rest)
            else: vals2.append(x)
        res |= trans_concrete(r, vals2, varnames, depth + 1)
    return res

def trans(r, P):
    vals = []; names = []
    for i, x in enumerate(P):
        if isinstance(x, int): vals.append(Lin(x))
        else:
            nm = 'v%d' % i; names.append(nm)
            vals.append(Lin(base(x[1]), {nm: MOD}))
    return trans_concrete(r, vals, names)

def work(st):
    r, P = st
    try:
        return ('OK', trans(r, P))
    except Touched:
        return ('UNFOLD', None)
    except Halt as h:
        return ('HALT', None)
    except Exception as e:
        return (type(e).__name__, str(e)[:200])

def explore(starts, procs=2):
    from multiprocessing import Pool
    pool = Pool(procs)
    seen = set(starts); q = deque(starts); flags = Counter(); ex = {}; edges = []
    while q and len(seen) < LIMIT:
        batch = [q.popleft() for _ in range(min(len(q), 200))]
        for st, (kind, res) in zip(batch, pool.map(work, batch, chunksize=4)):
            r, P = st
            if kind == 'UNFOLD':
                flags['unfold'] += 1
                if len(P) >= 11 and flags['deepunfold'] < 40:
                    flags['deepunfold'] += 1; print('DEEP', r, P, file=sys.stderr, flush=True)
                for g in LT_GAPS:
                    for u in UNITS:
                        s2 = (r, P + (g,) + u)
                        if s2 not in seen: seen.add(s2); q.append(s2)
                edges.append((st, 'UNFOLD')); continue
            if kind != 'OK':
                flags[kind] += 1; ex.setdefault(kind, []).append((st, res)); edges.append((st, kind)); continue
            edges.append((st, sorted(res, key=str)))
            for s2 in res:
                if len(s2[1]) > 21: flags['LONG'] += 1; ex.setdefault('LONG', []).append(s2); continue
                if s2 not in seen: seen.add(s2); q.append(s2)
        hist = Counter(len(P) for r, P in seen)
        print('progress', len(seen), len(q), len(edges), dict(flags), dict(sorted(hist.items())), flush=True, file=sys.stderr)
    return seen, flags, ex, q, edges

if __name__ == '__main__':
    starts = [(r, (a,)) for r in (1, 3) for a in FRONT_BLOCKS]
    seen, flags, ex, q, edges = explore(starts)
    print('SMALL', SMALL, 'MOD', MOD)
    print('states', len(seen), 'pending', len(q), 'processed', len(edges), 'flags', dict(flags))
    for k, v in ex.items():
        print(k, len(v))
        for e in v[:8]: print('   ', e)
    fr = Counter((r, P[0]) for r, P in seen)
    print('front classes', sorted(fr.items(), key=str))
    print('r=2 fronts', sorted({P[0] for r, P in seen if r == 2}, key=str))
    json.dump({'states': [[r, [list(x) if isinstance(x, tuple) else x for x in P]] for r, P in seen],
               'edges': [[[e[0][0], [list(x) if isinstance(x, tuple) else x for x in e[0][1]]],
                          e[1] if isinstance(e[1], str) else [[a, [list(x) if isinstance(x, tuple) else x for x in b]] for a, b in e[1]]]
                         for e in edges]},
              open('/tmp/an83/absym_%d_%d.json' % (SMALL, MOD), 'w'))
