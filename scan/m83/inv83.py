"""Check that the language L* is invariant under the exact Bell map of no. 83:
   L* = { r in {1,2,3}, N >= 100, S = 1^a (0^g 1^b)* T  with a >= 5, every b >= 6, every g >= 1 }.
Tree search over front prefixes; a prefix is extended (by all classes of (g, b)) only when the Bell step reads
the unknown rest.  Each leaf is one exact symbolic Bell step valid for all values in its classes and all N in the
residue class.  Output: number of leaves, failures (output not in L*, HALT, other)."""
import sys, os, pickle
sys.path.insert(0, '/tmp/an83')
from sym import Lin, L, Halt, Touched, NeedSplit
import symbell
from collections import Counter

SMALL = int(os.environ.get('SMALL', '8')); MOD = 4
def base(c):
    v = SMALL + 1
    while v % MOD != c: v += 1
    return v
def B(c): return ('B', c)
FRONT = list(range(5, SMALL + 1)) + [B(c) for c in range(MOD)]
BLK = list(range(6, SMALL + 1)) + [B(c) for c in range(MOD)]
GAP = list(range(1, SMALL + 1)) + [B(c) for c in range(MOD)]

def tolin(P):
    vals = []; names = []
    for i, x in enumerate(P):
        if isinstance(x, int): vals.append(Lin(x))
        else:
            nm = 'v%d' % i; names.append(nm); vals.append(Lin(base(x[1]), {nm: MOD}))
    return vals, names

def check_out(out):
    """out: list of (word, Lin) after the leading 0^r'; must be 1^a (0^g 1^b)* [0^g]; a >= 5, b >= 6."""
    if not out: return 'empty'
    if out[0][0] != '1': return 'starts with 0'
    for i, (w, e) in enumerate(out):
        if w == '1':
            lo = 5 if i == 0 else 6
            if e.c < lo: return 'short block %s at %d' % (e, i)
    return None

def step(r, c0, vals, names, depth=0):
    """returns list of results for this (r, c0, vals) handling NeedSplit by splitting vars."""
    try:
        M, r2, out = symbell.symbell(L(c0, n=4), r, vals)
    except NeedSplit as ns:
        w, e = ns.args[0]
        vs = [k for k in sorted(e.v) if k in names]
        if not vs or depth > 14: return [('NEEDSPLIT', str(ns))]
        v = vs[0]; res = []
        for sub in (0, 1):
            vals2 = []
            for x in vals:
                if v in x.v:
                    k = x.v[v]; rest = Lin(x.c, {a: b for a, b in x.v.items() if a != v})
                    vals2.append(rest + Lin(k, {v: k}) if sub else rest)
                else: vals2.append(x)
            res += step(r, c0, vals2, names, depth + 1)
        return res
    except Touched: return [('TOUCH', None)]
    except Halt: return [('HALT', None)]
    except Exception as e: return [(type(e).__name__, str(e)[:200])]
    if r2 not in (1, 2, 3): return [('BAD r', r2)]
    dM = M - L(c0, n=4)
    if not dM.nonneg() or dM.c <= 0: return [('N not growing', str(M))]
    bad = check_out(out)
    if bad: return [('OUT', bad + ' | ' + ' '.join('%s^%s' % (w, e) for w, e in out))]
    return [('OK', None)]

def work(task):
    r, c0, P = task
    vals, names = tolin(P)
    res = step(r, c0, vals, names)
    kinds = {k for k, _ in res}
    if 'TOUCH' in kinds: return (task, 'TOUCH', None)
    bad = [x for x in res if x[0] != 'OK']
    return (task, 'OK' if not bad else 'FAIL', bad[:3])

if __name__ == '__main__':
    from multiprocessing import Pool
    maxdepth = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    tasks = [(r, c0, (a,)) for r in (1, 2, 3) for c0 in (100, 101, 102, 103) for a in FRONT]
    stats = Counter(); fails = []; deep = Counter()
    pool = Pool(2)
    while tasks:
        nxt = []
        for task, kind, info in pool.imap_unordered(work, tasks, chunksize=8):
            r, c0, P = task
            stats[kind] += 1
            if kind == 'TOUCH':
                if len(P) >= maxdepth: stats['TOO DEEP'] += 1; deep[P[:5]] += 1; continue
                for g in GAP:
                    for b in BLK: nxt.append((r, c0, P + (g, b)))
            elif kind == 'FAIL':
                fails.append((task, info))
        print('level done', dict(stats), 'next', len(nxt), flush=True)
        tasks = nxt
    print('RESULT', dict(stats))
    print('fails', len(fails))
    for f in fails[:40]: print('  ', f)
    print('too deep examples', deep.most_common(10))
    pickle.dump((stats, fails, deep), open('/tmp/an83/inv83_result.pkl', 'wb'))
