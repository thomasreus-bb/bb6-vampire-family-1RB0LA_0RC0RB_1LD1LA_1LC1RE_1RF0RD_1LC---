"""Closure of the abstract Bell map of no. 83 with exact symbolic Bell steps (version 2).

Abstract state (r, par, P):
  r   = gap in front of S (1, 2, 3)
  par = parity of N (N = 4n + c0 with c0 in {101, 103} if par = 1, {100, 102} if par = 0), N >= 100
  P   = explicit runs of S (block, gap, ..., block); a run value is an exact int <= SMALL or ('B', c) = any value
        > SMALL with value = c (mod MOD).
  After P comes an arbitrary tail T in the tail language Lt: T = (g u)*, g a gap class in TGAPS (all values >= 4),
  u a unit from UNITS (a cluster of blocks joined by gaps < 4).
Every transition is computed exactly (for all values of the classes) with symbell.py; outputs are abstracted.
"""
import sys, json
sys.path.insert(0, '/tmp/an83')
from sym import Lin, L, Halt, Touched, NeedSplit, REST
import symbell
from collections import deque, Counter

SMALL, MOD = 12, 4
def base(c):
    v = SMALL + 1
    while v % MOD != c: v += 1
    return v
def B(c): return ('B', c)
TGAPS = list(range(4, SMALL + 1)) + [B(c) for c in range(MOD)]
TGS = set(TGAPS)
FRONT_BLOCKS = list(range(6, SMALL + 1, 2)) + [B(0), B(2)]

class Ambig(Exception): pass

def absval(e, names):
    if any(k not in names for k in e.v): raise ValueError(('foreign var', str(e)))
    if not e.v: return e.c if e.c <= SMALL else B(e.c % MOD)
    if any(x % MOD for x in e.v.values()): raise ValueError(('coef', str(e)))
    if e.c > SMALL: return B(e.c % MOD)
    raise Ambig(e)

def fold(P, UNITS):
    P = list(P)
    changed = True
    while changed:
        changed = False
        for u in UNITS:
            k = len(u)
            if len(P) > k + 1 and tuple(P[-k:]) == u and P[-k - 1] in TGS:
                # the unit must be a maximal cluster: the gap before it is >= 4 (in TGS) -- ok
                P = P[:-k - 1]; changed = True; break
    return tuple(P)

def split(r, par, vals, names, v, UNITS, depth):
    res = set()
    for sub in (0, 1):
        vals2 = []
        for x in vals:
            if v in x.v:
                k = x.v[v]; rest = Lin(x.c, {a: b for a, b in x.v.items() if a != v})
                vals2.append(rest + Lin(k, {v: k}) if sub else rest)
            else: vals2.append(x)
        res |= trans_c(r, par, vals2, names, UNITS, depth + 1)
    return res

def trans_c(r, par, vals, names, UNITS, depth=0):
    succ = set()
    for c0 in ((101, 103) if par else (100, 102)):
        N = L(c0, n=4)
        try:
            M, r2, out = symbell.symbell(N, r, vals)
        except NeedSplit as ns:
            w, e = ns.args[0]
            vs = [k for k in sorted(e.v) if k in names]
            if not vs or depth > 12: raise
            succ |= split(r, par, vals, names, vs[0], UNITS, depth); continue
        dM = M - N
        if not dM.nonneg() or dM.c <= 0: raise ValueError(('M<=N', str(M)))
        if any(x % 2 for x in M.v.values()):
            pars = (0, 1)
        else:
            pars = (M.c % 2,)
        if not out or out[0][0] != '1' or len(out) % 2 == 0: raise Touched()
        try:
            P2 = tuple(absval(e, names) for w, e in out)
        except Ambig as a:
            e = a.args[0]
            if depth > 12: raise ValueError(('deep ambig', str(e)))
            succ |= split(r, par, vals, names, sorted(e.v)[0], UNITS, depth); continue
        P2 = fold(P2, UNITS)
        for p2 in pars: succ.add((r2, p2, P2))
    return succ

def trans(st, UNITS):
    r, par, P = st
    vals = []; names = []
    for i, x in enumerate(P):
        if isinstance(x, int): vals.append(Lin(x))
        else:
            nm = 'v%d' % i; names.append(nm); vals.append(Lin(base(x[1]), {nm: MOD}))
    return trans_c(r, par, vals, names, UNITS)

_UNITS = None
def init(units):
    global _UNITS; _UNITS = units
def work(st):
    try: return ('OK', trans(st, _UNITS))
    except Touched: return ('UNFOLD', None)
    except Halt: return ('HALT', None)
    except Exception as e: return (type(e).__name__, str(e)[:200])

def explore(starts, UNITS, limit, maxlen, procs=2, log=sys.stderr):
    from multiprocessing import Pool
    pool = Pool(procs, initializer=init, initargs=(UNITS,))
    seen = set(starts); q = deque(starts); flags = Counter(); ex = {}; edges = {}
    while q and len(seen) < limit:
        batch = [q.popleft() for _ in range(min(len(q), 200))]
        for st, (kind, res) in zip(batch, pool.map(work, batch, chunksize=4)):
            r, par, P = st
            if kind == 'UNFOLD':
                flags['unfold'] += 1; edges[st] = 'UNFOLD'
                for g in TGAPS:
                    for u in UNITS:
                        s2 = (r, par, P + (g,) + u)
                        if s2 not in seen: seen.add(s2); q.append(s2)
                continue
            if kind != 'OK':
                flags[kind] += 1; ex.setdefault(kind, []).append((st, res)); edges[st] = kind; continue
            edges[st] = sorted(res, key=str)
            for s2 in res:
                if len(s2[2]) > maxlen: flags['LONG'] += 1; ex.setdefault('LONG', []).append(s2); continue
                if s2 not in seen: seen.add(s2); q.append(s2)
        hist = Counter(len(P) for r, p, P in seen)
        print('progress', len(seen), len(q), len(edges), dict(flags), dict(sorted(hist.items())), flush=True, file=log)
    pool.close()
    return seen, flags, ex, q, edges

def clusters_at_end(P):
    """split the suffix of P into (gap, cluster) pairs from the end as long as gaps before clusters are >= 4."""
    out = []; i = len(P)
    while i > 1:
        j = i - 1          # P[j] is a block
        while j >= 2 and P[j - 1] not in TGS and isinstance(P[j - 1], int) and P[j - 1] < 4:
            j -= 2
        if j < 1: break
        if P[j - 1] in TGS:
            out.append(tuple(P[j:i])); i = j - 1
        else: break
    return out

if __name__ == '__main__':
    UNITS = [(6,), (12,), (6, 2, 6)]
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    maxlen = int(sys.argv[2]) if len(sys.argv) > 2 else 21
    rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    for rnd in range(rounds):
        starts = [(r, 1, (a,)) for r in (1, 3) for a in FRONT_BLOCKS]
        seen, flags, ex, q, edges = explore(starts, UNITS, limit, maxlen)
        print('ROUND', rnd, 'units', UNITS, 'states', len(seen), 'pending', len(q), 'flags', dict(flags), flush=True)
        for k, v in ex.items():
            print('  ', k, len(v), v[:4], flush=True)
        # learn new units from long states
        cand = Counter()
        for r, par, P in seen:
            if len(P) >= 9:
                for u in clusters_at_end(P[1:]):
                    if u not in UNITS: cand[u] += 1
        print('  candidate units', cand.most_common(12), flush=True)
        if not q and not flags.get('LONG') and not cand:
            print('CLOSED', flush=True); break
        new = [u for u, c in cand.most_common(6)]
        if not new: break
        UNITS = UNITS + new
    json.dump({'units': UNITS, 'states': [[r, p, [list(x) if isinstance(x, tuple) else x for x in P]] for r, p, P in seen],
               'flags': dict(flags)}, open('/tmp/an83/absym2_result.json', 'w'))
