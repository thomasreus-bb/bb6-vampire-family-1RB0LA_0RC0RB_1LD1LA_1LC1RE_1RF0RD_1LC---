"""Invariance check for no. 83 with a language of local constraints around special runs (heuristic transitions
via the C batch simulator cycb; the closed language is to be verified afterwards with the exact symbolic step).

Runs are abstracted to classes (exact <= SMALL, else ('B', v mod 4)).
normal gap  = even >= 4 ;  normal block = even >= 6 ;  everything else is special.
Language L(Q): for every special run at position i, the window W(i) = (tag, runs[i-R .. i+R]) is in Q, where
missing positions before the start are None and tag = (r, par) if i - R <= 0 else ('d', i % 2).
Normal runs are otherwise unconstrained.  Q is learned (missing windows are added) until closed.
"""
import sys, os, pickle, time, random, re, subprocess
sys.path.insert(0, '/tmp/an83')
from collections import Counter, defaultdict, deque

SMALL = int(os.environ.get('SMALL', '12')); MOD = 4
RAD = int(os.environ.get('RAD', '2'))
MAXLEN = int(os.environ.get('MAXLEN', '17'))
def B(c): return ('B', c)
def cls(v): return v if v <= SMALL else B(v % MOD)
def val_even(x): return (x % 2 == 0) if isinstance(x, int) else (x[1] % 2 == 0)
def val_ge(x, k): return x >= k if isinstance(x, int) else True
CHAINS = ((6, 2), (11, 5))      # (block, gap) patterns that form chains b (g b)^k
KMAX_EXACT = 3
def is_chain(x): return isinstance(x, tuple) and x[0] == 'C'
def kcls(k): return k if k <= KMAX_EXACT else ('K', k % 2)
def is_special(i, x):
    if is_chain(x): return True
    if i % 2 == 1: return not (val_even(x) and val_ge(x, 4))
    return not (val_even(x) and val_ge(x, 6))
def compress(runs):
    """concrete runs -> items (chains of length k >= 2 become ('C', b, g, kclass))"""
    out = []; i = 0; n = len(runs)
    while i < n:
        if i % 2 == 0 or (len(out) % 2 == 0):
            pass
        x = runs[i]
        if len(out) % 2 == 0:   # block position
            done = False
            for b, g in CHAINS:
                if x == b:
                    j = i; k = 0
                    while j + 2 < n and runs[j + 1] == g and runs[j + 2] == b: j += 2; k += 1
                    if k >= 2:
                        out.append(('C', b, g, kcls(k))); i = j + 1; done = True; break
            if done: continue
            out.append(cls(x)); i += 1
        else:
            out.append(cls(x)); i += 1
    return tuple(out)
GAPS = list(range(1, SMALL + 1)) + [B(c) for c in range(MOD)]
BLKS = list(range(1, SMALL + 1)) + [B(c) for c in range(MOD)] + [('C', b, g, k) for b, g in CHAINS for k in (2, 3, ('K', 0), ('K', 1))]
NGAPS = [x for x in GAPS if not is_special(1, x)]
NBLKS = [x for x in BLKS if not is_special(0, x)]

def win(r, par, P, i):
    lo = i - RAD
    t = (r, par) if lo <= 0 else ('d', i % 2)
    return (t,) + tuple(P[j] if 0 <= j < len(P) else None for j in range(lo, i + RAD + 1))

def special_windows(r, par, P, upto=None):
    """windows of special runs whose window lies completely inside P (or before its start)"""
    out = []
    for i, x in enumerate(P):
        if is_special(i, x) and i + RAD < len(P):
            out.append(win(r, par, P, i))
    return out

def pending_specials(P):
    return [i for i, x in enumerate(P) if is_special(i, x) and i + RAD >= len(P)]

# ---------------- transitions (heuristic, cycb) ----------------
TAIL1 = (97, 6, 89, 6, 103, 6)
TAIL2 = (8, 12, 4, 6, 10, 6)
_proc = None
def runb(N, r, runs):
    global _proc
    if _proc is None:
        _proc = subprocess.Popen(['/tmp/an83/cycb'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    S = ''.join(('1' if i % 2 == 0 else '0') * x for i, x in enumerate(runs))
    _proc.stdin.write('%d %d %s 4000000000\n' % (N, r, S)); _proc.stdin.flush()
    o = _proc.stdout.readline().split()
    if o[0] != 'BELL': return (o[0],)
    return ('BELL', int(o[1]), int(o[2]), [len(m.group(0)) for m in re.finditer(r'0+|1+', o[3])])

def conc(P, rnd, mode):
    """returns (runs, item_lengths)"""
    out = []; lens = []
    for x in P:
        if isinstance(x, int): out.append(x); lens.append(1)
        elif is_chain(x):
            _, b, g, k = x
            if isinstance(k, tuple): k = 4 + k[1] + (0 if mode == 0 else 2 * rnd.randrange(1, 4))
            seg = [b] + [g, b] * k; out += seg; lens.append(len(seg))
        else:
            v = SMALL + 1
            while v % MOD != x[1]: v += 1
            out.append(v if mode == 0 else v + MOD * rnd.randrange(1, 12)); lens.append(1)
    return out, lens

def work(task):
    r, par, P = task
    rnd = random.Random(hash(task) & 0xffffffff)
    succ = set()
    try:
        for mode in (0, 1, 2):
            vals, lens = conc(P, rnd, mode)
            ctxlen = sum(lens[-RAD:])
            Ns = [8 * b + c for b in (60 + rnd.randrange(10), 90 + rnd.randrange(10)) for c in ((1, 3) if par else (0, 2))]
            first = {}
            for tail in (TAIL1, TAIL2):
                for N in (Ns if tail is TAIL1 else Ns[:1]):
                    o = runb(N, r, vals + list(tail))
                    if o[0] == 'HALT': return task, 'HALT', (vals, N)
                    if o[0] != 'BELL': return task, o[0], (vals, N)
                    M, r2, R = o[1:]
                    if len(R) < len(tail) or tuple(R[-len(tail):]) != tail: return task, 'TOUCH', None
                    R = tuple(R[:-len(tail)])
                    if N == Ns[0]:
                        if tail in first: pass
                        first[tail] = (M, r2, R)
                    if tail is TAIL1:
                        if len(R) % 2 == 0 or len(R) < ctxlen + 1 or list(R[-ctxlen:]) != vals[-ctxlen:]: return task, 'TOUCH', None
                        if M <= N: return task, 'NGROW', (vals, N, M)
                        items = compress(R)
                        if tuple(items[-RAD:]) != tuple(P[-RAD:]): return task, 'TOUCH', None
                        succ.add((r2, M % 2, items))
            if first[TAIL1] != first[TAIL2]: return task, 'TOUCH', None
        return task, 'OK', succ
    except Exception as e:
        return task, type(e).__name__, str(e)[:200]

# ---------------- language enumeration ----------------
def allowed_prefix(r, par, P, Q, Qpre):
    """all complete special windows in Q; incomplete ones must be prefixes of some window in Q"""
    for w in special_windows(r, par, P):
        if w not in Q: return False
    for i in pending_specials(P):
        w = win(r, par, P, i)
        k = 1 + RAD + (len(P) - i)     # number of known entries (tag + runs up to the end of P)
        if w[:k] not in Qpre: return False
    return True

def extend(r, par, P, Q, Qpre):
    out = []
    for g in GAPS:
        for b in BLKS:
            P2 = P + (g, b)
            if allowed_prefix(r, par, P2, Q, Qpre): out.append((r, par, P2))
    return out

def check(Q, CACHE, procs=2, log=sys.stderr):
    from multiprocessing import Pool
    Qpre = set()
    for w in Q:
        for k in range(1, len(w) + 1): Qpre.add(w[:k])
    starts = []
    for r in (1, 2, 3):
        for par in (0, 1):
            for a in BLKS:
                if allowed_prefix(r, par, (a,), Q, Qpre) and (is_special(0, a) or (r in (1, 3) and par == 1)):
                    starts.append((r, par, (a,)))
    todo = starts; missing = Counter(); stats = Counter(); fails = []
    pool = Pool(procs)
    while todo:
        new = [t for t in todo if t not in CACHE]
        for task, kind, res in pool.imap_unordered(work, new, chunksize=16):
            CACHE[task] = (kind, res)
        nxt = []
        for t in todo:
            kind, res = CACHE[t]; stats[kind] += 1
            r, par, P = t
            if kind == 'TOUCH':
                if len(P) >= MAXLEN: stats['TOODEEP'] += 1; fails.append((t, 'TOODEEP')); continue
                nxt += extend(r, par, P, Q, Qpre)
            elif kind == 'OK':
                needmore = False
                for (r2, p2, P2) in res:
                    for i in pending_specials(P2):
                        d = len(P2) - i; j = len(P) - d
                        if not (0 <= j < len(P) and P[j] == P2[i] and tuple(P[j - RAD:]) == tuple(P2[i - RAD:])): needmore = True
                if needmore:
                    stats['TOUCH2'] += 1
                    if len(P) >= MAXLEN: stats['TOODEEP'] += 1; fails.append((t, 'TOODEEP')); continue
                    nxt += extend(r, par, P, Q, Qpre); continue
                for (r2, p2, P2) in res:
                    for w in special_windows(r2, p2, P2):
                        if w not in Q: missing[w] += 1
                    # specials too close to the end of the output: their window needs runs of T
                    for i in pending_specials(P2):
                        if i < len(P2) - RAD:  # cannot happen (pending means i+RAD >= len)
                            pass
                        # the window continues into T; T after the output is the same T as after the input,
                        # whose first runs are not known here -> accept only if the special was already present
                        # at the same distance from the end in the input (unchanged context).
                        d = len(P2) - i
                        j = len(P) - d
                        if not (0 <= j < len(P) and P[j] == P2[i] and tuple(P[j - RAD:]) == tuple(P2[i - RAD:])):
                            missing[('PENDING',) + win(r2, p2, P2, i)] += 1
            else:
                fails.append((t, kind, res))
        print('level', dict(stats), 'next', len(nxt), 'missing', len(missing), flush=True, file=log)
        todo = list(set(nxt))
    pool.close()
    return stats, missing, fails

def initial_Q():
    confs = pickle.load(open('/tmp/an83/coinconfs.pkl', 'rb'))
    Q = set()
    for r, par, runs in confs:
        R = list(runs)
        if len(R) % 2 == 0: R = R[:-1]
        a = compress(R[:-2])
        Q.update(special_windows(r, par, a))
    for l in open('/tmp/an83/orb83.txt'):
        p = l.split()
        if not p[0].isdigit(): continue
        a = compress([int(x[1:]) for x in p[4:]][:-2])
        Q.update(special_windows(int(p[3]), int(p[2]) % 2, a))
    return Q

if __name__ == '__main__':
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    Q = initial_Q()
    print('initial Q', len(Q), flush=True)
    CACHE = {}
    for rd in range(rounds):
        t0 = time.time()
        stats, missing, fails = check(Q, CACHE)
        pend = [w for w in missing if w[0] == 'PENDING']
        miss = {w: c for w, c in missing.items() if w[0] != 'PENDING'}
        print('ROUND', rd, 'Q', len(Q), 'stats', dict(stats), 'missing', len(miss), 'pending', len(pend), 'fails', len(fails),
              '%.0fs' % (time.time() - t0), flush=True)
        kinds = Counter(f[1] for f in fails)
        print('   fail kinds', dict(kinds), flush=True)
        for f in [f for f in fails if f[1] == 'HALT'][:10]: print('   HALT', f, flush=True)
        for f in [f for f in fails if f[1] != 'HALT'][:6]: print('   ', f, flush=True)
        for w in pend[:5]: print('   pending', w, flush=True)
        pickle.dump((Q, missing, fails), open('/tmp/an83/inv6h_round.pkl', 'wb'))
        if kinds.get('HALT'): print('HALT inside the language', flush=True); break
        if not miss and not fails and not pend: print('CLOSED (heuristic)', flush=True); break
        Q |= set(miss)
        # a pending special: add the windows it could have with any continuation of known specials (learned later)
