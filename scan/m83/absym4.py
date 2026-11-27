"""Closure of the abstract Bell map of no. 83 with a k-window (factor) tail language, learned iteratively.

State (r, par, P): r = gap in front of S, par = N mod 2, P = explicit runs (block, gap, ..., block).
Values: exact ints <= SMALL or ('B', c) (> SMALL, = c mod MOD).
Tail T after P: any continuation (gap, block, gap, ...) such that every window of K consecutive runs of the whole
word P+T (from position START on) lies in the window set F.  The last K-1 runs of P are the context of T.
Every Bell step is exact (symbell.py).  A step that changes one of the K-1 context runs counts as touching T.
"""
import sys, json, os, pickle
sys.path.insert(0, '/tmp/an83')
from sym import Lin, L, Halt, Touched, NeedSplit
import symbell
from collections import deque, Counter

SMALL = int(os.environ.get('SMALL', '8')); MOD = 4
K = int(os.environ.get('KWIN', '3'))
KEEP = int(os.environ.get('KEEP', '3'))      # front runs that are never folded
MAXLEN = int(os.environ.get('MAXLEN', '21'))
def base(c):
    v = SMALL + 1
    while v % MOD != c: v += 1
    return v
def B(c): return ('B', c)
VALS = list(range(1, SMALL + 1)) + [B(c) for c in range(MOD)]

def cls(v):
    return v if v <= SMALL else B(v % MOD)

class Ambig(Exception): pass
def absval(e, names):
    if any(k not in names for k in e.v): raise ValueError(('foreign var', str(e)))
    if not e.v: return cls(e.c)
    if any(x % MOD for x in e.v.values()): raise ValueError(('coef', str(e)))
    if e.c > SMALL: return B(e.c % MOD)
    raise Ambig(e)

def win(P, i):
    """window of K runs starting at index i, tagged with parity of i (0 = starts with a block)"""
    return (i % 2,) + tuple(P[i:i + K])

def windows_ok(P, F, lo):
    """all windows of P that end at an index >= lo are in F"""
    bad = []
    for i in range(max(0, lo - K + 1), len(P) - K + 1):
        w = win(P, i)
        if w not in F: bad.append(w)
    return bad

def fold(P, F):
    P = list(P)
    while len(P) >= KEEP + (K - 1) + 2:
        # drop the last pair (gap, block); it becomes the start of T. New windows that must be allowed: those that
        # contain the dropped pair together with runs before it (they were not constrained before only if they
        # overlap the explicit part, so check all windows touching the last K-1+2 runs).
        if windows_ok(P, F, len(P) - 2): break
        P = P[:-2]
    return tuple(P)

def split(st, vals, names, v, F, depth):
    res = set()
    for sub in (0, 1):
        vals2 = []
        for x in vals:
            if v in x.v:
                k = x.v[v]; rest = Lin(x.c, {a: b for a, b in x.v.items() if a != v})
                vals2.append(rest + Lin(k, {v: k}) if sub else rest)
            else: vals2.append(x)
        res |= trans_c(st, vals2, names, F, depth + 1)
    return res

def trans_c(st, vals, names, F, depth=0):
    r, par, P = st
    succ = set()
    ctx_in = [str(x) for x in vals[-(K - 1):]] if len(vals) > KEEP else None
    for c0 in ((101, 103) if par else (100, 102)):
        N = L(c0, n=4)
        CALLS[0] += 1
        if CALLS[0] > 64: raise Budget()
        try:
            M, r2, out = symbell.symbell(N, r, vals)
        except NeedSplit as ns:
            w, e = ns.args[0]
            vs = [k for k in sorted(e.v) if k in names]
            if not vs or depth > 12: raise
            succ |= split(st, vals, names, vs[0], F, depth); continue
        dM = M - N
        if not dM.nonneg() or dM.c <= 0: raise ValueError(('M<=N', str(M)))
        pars = (0, 1) if any(x % 2 for x in M.v.values()) else (M.c % 2,)
        if not out or out[0][0] != '1' or len(out) % 2 == 0: raise Touched()
        # the context runs (last K-1 runs before T) must be unchanged
        if len(vals) > KEEP:
            if len(out) < K - 1 or [str(e) for w, e in out[-(K - 1):]] != ctx_in: raise Touched()
        else:
            raise Touched()     # P too short: always unfold until the context is separate from the front
        try:
            P2 = tuple(absval(e, names) for w, e in out)
        except Ambig as a:
            e = a.args[0]
            if depth > 12: raise ValueError(('deep ambig', str(e)))
            succ |= split(st, vals, names, sorted(e.v)[0], F, depth); continue
        for p2 in pars: succ.add((r2, p2, P2))
    return succ

class Budget(Exception): pass
CALLS = [0]
def trans(st, F):
    CALLS[0] = 0
    r, par, P = st
    vals = []; names = []
    for i, x in enumerate(P):
        if isinstance(x, int): vals.append(Lin(x))
        else:
            nm = 'v%d' % i; names.append(nm); vals.append(Lin(base(x[1]), {nm: MOD}))
    return trans_c(st, vals, names, F)

def unfold(P, F):
    out = []
    for g in VALS:
        for b in VALS:
            P2 = P + (g, b)
            if not windows_ok(P2, F, len(P)): out.append(P2)
    return out

_F = None
def init(F):
    global _F; _F = F
def work(st):
    try: return ('OK', trans(st, _F))
    except Touched: return ('UNFOLD', None)
    except Halt: return ('HALT', None)
    except Exception as e: return (type(e).__name__, str(e)[:300])

CACHE = {}
def explore(starts, F, limit, procs=2, log=sys.stderr):
    from multiprocessing import Pool
    pool = Pool(procs, initializer=init, initargs=(F,))
    seen = set(starts); q = deque(starts); flags = Counter(); ex = {}; newwin = Counter(); edges = {}
    while q and len(seen) < limit:
        batch = [q.popleft() for _ in range(min(len(q), 400))]
        todo = [st for st in batch if st not in CACHE]
        for st, res in zip(todo, pool.map(work, todo, chunksize=4)): CACHE[st] = res
        for st, (kind, res) in [(st, CACHE[st]) for st in batch]:
            if kind == 'OK': res = {(a, b, fold(c, F)) for a, b, c in res}
            r, par, P = st
            if kind == 'UNFOLD':
                flags['unfold'] += 1; edges[st] = 'UNFOLD'
                kids = unfold(P, F)
                if not kids: flags['deadend'] += 1
                for P2 in kids:
                    s2 = (r, par, P2)
                    if s2 not in seen: seen.add(s2); q.append(s2)
                continue
            if kind != 'OK':
                flags[kind] += 1; ex.setdefault(kind, []).append((st, res)); edges[st] = kind; continue
            edges[st] = sorted(res, key=str)
            for s2 in res:
                if len(s2[2]) > MAXLEN:
                    flags['LONG'] += 1
                    for w in windows_ok(s2[2], F, KEEP): newwin[w] += 1
                    continue
                if s2 not in seen: seen.add(s2); q.append(s2)
        if len(edges) % 8000 < 400:
            pickle.dump(CACHE, open('/tmp/an83/absym4_cache_K%d_S%d.pkl' % (K, SMALL), 'wb'))
        hist = Counter(len(P) for r, p, P in seen)
        print('progress', len(seen), len(q), len(edges), len(F), dict(flags), dict(sorted(hist.items())), flush=True, file=log)
    pool.close()
    return seen, flags, ex, q, edges, newwin

def orbit_configs(path='/tmp/an83/orb83.txt'):
    out = []
    for l in open(path):
        p = l.split()
        if not p[0].isdigit(): continue
        out.append((int(p[0]), int(p[2]) % 2, int(p[3]), [int(x[1:]) for x in p[4:]]))
    return out

if __name__ == '__main__':
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    orb = orbit_configs()
    if os.path.exists('/tmp/an83/absym4_cache_K%d_S%d.pkl' % (K, SMALL) + ''):
        CACHE.update(pickle.load(open('/tmp/an83/absym4_cache_K%d_S%d.pkl' % (K, SMALL) + '', 'rb')))
    F = set()
    for k, par, r, runs in orb:
        a = [cls(x) for x in runs]
        for i in range(KEEP, len(a) - K + 1): F.add(win(a, i))
    cf = '/tmp/an83/coinF_K%d.pkl' % K
    if os.path.exists(cf): F |= pickle.load(open(cf, 'rb'))
    # start: the real configuration at the last orbit Bell
    k, par, r, runs = orb[-1]
    a = tuple(cls(x) for x in runs)
    assert not windows_ok(a, F, KEEP)
    P0 = fold(a, F)
    starts = [(r, par, P0)]
    print('start Bell', k, 'r', r, 'par', par, 'P0', P0, 'F', len(F), flush=True)
    for rd in range(rounds):
        seen, flags, ex, q, edges, newwin = explore(starts, F, limit)
        print('ROUND', rd, 'F', len(F), 'states', len(seen), 'pending', len(q), 'flags', dict(flags), flush=True)
        for kk, v in ex.items(): print('  ', kk, len(v), v[:4], flush=True)
        pickle.dump((F, seen, edges, flags, ex), open('/tmp/an83/absym4_last.pkl', 'wb'))
        pickle.dump(CACHE, open('/tmp/an83/absym4_cache_K%d_S%d.pkl' % (K, SMALL) + '', 'wb'))
        if flags.get('HALT'): print('HALT found', flush=True); break
        for r_, p_, P_ in seen:
            if len(P_) >= KEEP + K + 2:
                for w in windows_ok(P_, F, KEEP): newwin[w] += 1
        if not q and not newwin:
            print('CLOSED: no pending states, no new windows', flush=True); break
        print('  new windows', len(newwin), newwin.most_common(10), flush=True)
        F |= set(newwin)
