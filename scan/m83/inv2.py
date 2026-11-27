"""Invariance check of a window language for the Bell map of no. 83 (CTL-style, with learning).

Configuration at a Bell: (r, par, S) with S = run lengths (block, gap, block, ...), N >= 100 with parity par.
Run values are abstracted to classes: exact <= SMALL, else ('B', v mod MOD).
Language L(F): all windows W_i = (tag(i), S[i:i+K]) are in F, where tag(0) = (r, par, 0), tag(i) = i for
i = 1, 2, and tag(i) = 3 + i % 2 for i >= 3  (positions >= 3 are treated alike up to parity).
Check: for every configuration in L(F), the Bell map gives a configuration in L(F) and does not halt.
Configurations are enumerated as prefixes; a prefix is extended (consistently with F) only when the exact
symbolic Bell step reads beyond it or changes its last K-1 runs.  Missing windows are learned (added to F) and the
check is repeated until nothing new appears.
"""
import sys, os, pickle, time
sys.path.insert(0, '/tmp/an83')
from sym import Lin, L, Halt, Touched, NeedSplit
import symbell
from collections import Counter, defaultdict

SMALL = int(os.environ.get('SMALL', '8')); MOD = 4
K = int(os.environ.get('KWIN', '3'))
MINDEEP = 3 + K          # explicit prefix length needed so that T stays at deep positions
def base(c):
    v = SMALL + 1
    while v % MOD != c: v += 1
    return v
def B(c): return ('B', c)
def cls(v): return v if v <= SMALL else B(v % MOD)
def tag(i, r=None, par=None):
    if i == 0: return (r, par, 0)
    if i < 3: return i
    return 3 + i % 2
def windows(r, par, P, lo=0, hi=None):
    hi = len(P) - K + 1 if hi is None else hi
    return [(tag(i, r, par),) + tuple(P[i:i + K]) for i in range(lo, max(lo, hi))]

class Ambig(Exception): pass
class Budget(Exception): pass
def absval(e, names):
    if any(k not in names for k in e.v): raise ValueError(('foreign var', str(e)))
    if not e.v: return cls(e.c)
    if any(x % MOD for x in e.v.values()): raise ValueError(('coef', str(e)))
    if e.c > SMALL: return B(e.c % MOD)
    raise Ambig(e)

def tolin(P):
    vals = []; names = []
    for i, x in enumerate(P):
        if isinstance(x, int): vals.append(Lin(x))
        else:
            nm = 'v%d' % i; names.append(nm); vals.append(Lin(base(x[1]), {nm: MOD}))
    return vals, names

def substitute(vals, v, sub):
    out = []
    for x in vals:
        if v in x.v:
            k = x.v[v]; rest = Lin(x.c, {a: b for a, b in x.v.items() if a != v})
            out.append(rest + Lin(k, {v: k}) if sub else rest)
        else: out.append(x)
    return out

def bell(r, par, vals, names, calls, depth=0):
    """exact successors {(r2, par2, P2)} of a prefix (raises Touched / Halt / ...)"""
    succ = set()
    for c0 in ((101, 103) if par else (100, 102)):
        calls[0] += 1
        if calls[0] > 200: raise Budget()
        try:
            M, r2, out = symbell.symbell(L(c0, n=4), r, vals)
        except NeedSplit as ns:
            w, e = ns.args[0]
            vs = [k for k in sorted(e.v) if k in names]
            if not vs or depth > 14: raise
            for sub in (0, 1): succ |= bell(r, par, substitute(vals, vs[0], sub), names, calls, depth + 1)
            continue
        dM = M - L(c0, n=4)
        if not dM.nonneg() or dM.c <= 0: raise ValueError(('M<=N', str(M)))
        pars = (0, 1) if any(x % 2 for x in M.v.values()) else (M.c % 2,)
        if not out or out[0][0] != '1' or len(out) % 2 == 0: raise Touched()
        if len(out) < MINDEEP or [str(e) for w, e in out[-(K - 1):]] != [str(x) for x in vals[-(K - 1):]]:
            raise Touched()
        try:
            P2 = tuple(absval(e, names) for w, e in out)
        except Ambig as a:
            e = a.args[0]
            if depth > 14: raise ValueError(('deep ambig', str(e)))
            v = sorted(e.v)[0]
            for sub in (0, 1): succ |= bell(r, par, substitute(vals, v, sub), names, calls, depth + 1)
            continue
        for p2 in pars: succ.add((r2, p2, P2))
    return succ

def work(task):
    r, par, P = task
    vals, names = tolin(P)
    try:
        return task, 'OK', bell(r, par, vals, names, [0])
    except Touched: return task, 'TOUCH', None
    except Halt: return task, 'HALT', None
    except Exception as e: return task, type(e).__name__, str(e)[:200]

def extensions(r, par, P, F, ext):
    """one more (gap, block) consistent with F at the new windows"""
    i = len(P) - K + 1      # first new window index after adding two runs: windows starting at i, i+1
    out = []
    for g, b in ext.get((tag(i, r, par),) + tuple(P[i:]) if K - 1 <= len(P) else None, ()):
        P2 = P + (g, b)
        ok = all(w in F for w in windows(r, par, P2, max(0, len(P2) - K - 1)))
        if ok: out.append(P2)
    return out

def build_ext(F):
    """map (tag, last K-1 runs) -> possible next two runs (gap, block), from pairs of overlapping windows"""
    byprefix = defaultdict(set)
    for w in F:
        byprefix[(w[0],) + w[1:K]].add(w[K])
    ext = defaultdict(set)
    for w in F:
        t, runs = w[0], w[1:]
        # w = window at index i with runs P[i..i+K-1]; we want: given P[i..i+K-2] (K-1 runs), next run = runs[-1]
        key = (t,) + runs[:K - 1]
        # second run after it: window at i+1 must start with runs[1:] ; its tag:
        ext[key].add(runs[K - 1])
    return ext

def check(F, CACHE, procs=2, maxlen=17, log=sys.stderr):
    from multiprocessing import Pool
    # one-step extension table: key (tag(i), P[i..i+K-2]) -> set of P[i+K-1]
    nxt = defaultdict(set)
    for w in F: nxt[(w[0],) + w[1:K]].add(w[K])
    def extend(r, par, P):
        out = []
        i = len(P) - (K - 1)
        for g in nxt.get((tag(i, r, par),) + tuple(P[i:]), ()):
            P1 = P + (g,)
            j = len(P1) - (K - 1)
            for b in nxt.get((tag(j, r, par),) + tuple(P1[j:]), ()):
                out.append((r, par, P1 + (b,)))
        return out
    # start prefixes: windows at position 0 (K runs; K odd -> ends with a block; K even -> extend once)
    starts = []
    for w in F:
        if isinstance(w[0], tuple):
            r, par, _ = w[0]; P = w[1:]
            if len(P) % 2 == 1: starts.append((r, par, P))
    todo = list(set(starts)); missing = Counter(); stats = Counter(); fails = []; done = 0
    pool = Pool(procs)
    while todo:
        new = [t for t in todo if t not in CACHE]
        for task, kind, res in pool.imap_unordered(work, new, chunksize=8):
            CACHE[task] = (kind, res)
        nxtodo = []
        for t in todo:
            kind, res = CACHE[t]; stats[kind] += 1; done += 1
            r, par, P = t
            if kind == 'TOUCH':
                if len(P) >= maxlen: stats['TOODEEP'] += 1; fails.append((t, 'TOODEEP')); continue
                nxtodo += extend(r, par, P)
            elif kind == 'OK':
                for (r2, p2, P2) in res:
                    # windows of the output that involve explicit runs (T windows are unchanged and already in F)
                    for w in windows(r2, p2, P2, 0, len(P2) - K + 1):
                        if w not in F: missing[w] += 1
            else:
                fails.append((t, kind, res))
        print('level', dict(stats), 'next', len(nxtodo), 'missing', len(missing), flush=True, file=log)
        todo = list(set(nxtodo))
    pool.close()
    return stats, missing, fails

if __name__ == '__main__':
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    confs = pickle.load(open('/tmp/an83/coinconfs.pkl', 'rb'))
    F = set()
    for r, par, runs in confs:
        a = [cls(x) for x in runs]
        if len(a) % 2 == 0: a = a[:-1]
        F.update(windows(r, par, a[:-2]))     # drop the last runs (truncation artefacts)
    for l in open('/tmp/an83/orb83.txt'):
        p = l.split()
        if not p[0].isdigit(): continue
        a = [cls(int(x[1:])) for x in p[4:]]
        F.update(windows(int(p[3]), int(p[2]) % 2, a[:-2]))
    print('initial F', len(F), flush=True)
    cpath = '/tmp/an83/inv2_cache_K%d_S%d.pkl' % (K, SMALL)
    CACHE = pickle.load(open(cpath, 'rb')) if os.path.exists(cpath) else {}
    for rd in range(rounds):
        t0 = time.time()
        stats, missing, fails = check(F, CACHE)
        pickle.dump(CACHE, open(cpath, 'wb'))
        print('ROUND', rd, 'F', len(F), 'stats', dict(stats), 'missing', len(missing), 'fails', len(fails),
              '%.0fs' % (time.time() - t0), flush=True)
        kinds = Counter(f[1] for f in fails)
        print('   fail kinds', dict(kinds), flush=True)
        for f in [f for f in fails if f[1] == 'HALT'][:10]: print('   HALT', f[0], flush=True)
        for f in [f for f in fails if f[1] not in ('HALT',)][:5]: print('   ', f, flush=True)
        pickle.dump((F, missing, fails), open('/tmp/an83/inv2_round.pkl', 'wb'))
        if kinds.get('HALT'): print('HALT reachable inside the language', flush=True); break
        if not missing and not fails: print('INVARIANT: L(F) is closed under the Bell map, no HALT', flush=True); break
        F |= set(missing)
