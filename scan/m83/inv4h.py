"""Fast heuristic version of the window-language invariance check (inv3.py) for no. 83.
Transitions are computed with the C batch simulator cycb on several concretizations of each abstract prefix
(3 value choices for big classes, 4 representatives of N in the residue class, a second tail to detect reads).
The final closed language must afterwards be verified with the exact symbolic step (inv3.py / verify)."""
import sys, os, pickle, time, random, re, subprocess
sys.path.insert(0, '/tmp/an83')
from collections import Counter, defaultdict
import inv3
from inv3 import cls, tag, windows, K, SMALL, MOD, B

TAIL1 = (97, 6, 89, 6, 103, 6)
TAIL2 = (4, 12, 2, 6, 10, 6)
_proc = None
def proc():
    global _proc
    if _proc is None:
        _proc = subprocess.Popen(['/tmp/an83/cycb'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
    return _proc
def runb(N, r, runs):
    S = ''.join(('1' if i % 2 == 0 else '0') * x for i, x in enumerate(runs))
    p = proc(); p.stdin.write('%d %d %s 4000000000\n' % (N, r, S)); p.stdin.flush()
    o = p.stdout.readline().split()
    if o[0] != 'BELL': return (o[0],)
    return ('BELL', int(o[1]), int(o[2]), [len(m.group(0)) for m in re.finditer(r'0+|1+', o[3])])

def conc_values(P, rnd, mode):
    out = []
    for x in P:
        if isinstance(x, int): out.append(x)
        else:
            c = x[1]; v = SMALL + 1
            while v % MOD != c: v += 1
            out.append(v if mode == 0 else v + MOD * rnd.randrange(1, 12))
    return out

def work(task):
    r, par, P = task
    rnd = random.Random(hash(task) & 0xffffffff)
    succ = set()
    try:
        for mode in (0, 1, 2):
            vals = conc_values(P, rnd, mode)
            res_by_tail = {}
            Ns = [8 * b + c for b in (60 + rnd.randrange(10), 90 + rnd.randrange(10)) for c in ((1, 3) if par else (0, 2))]
            for tail in (TAIL1, TAIL2):
                outs = []
                for N in (Ns if tail is TAIL1 else Ns[:1]):
                    o = runb(N, r, vals + list(tail))
                    if o[0] == 'HALT': return task, 'HALT', (vals, N)
                    if o[0] != 'BELL': return task, o[0], (vals, N)
                    M, r2, R = o[1], o[2], o[3]
                    if len(R) < len(tail) or tuple(R[-len(tail):]) != tail: return task, 'TOUCH', None
                    outs.append((N, M, r2, tuple(R[:-len(tail)])))
                res_by_tail[tail] = outs
            if res_by_tail[TAIL1][0][1:] != res_by_tail[TAIL2][0][1:]: return task, 'TOUCH', None
            for N, M, r2, R in res_by_tail[TAIL1]:
                if len(R) < K or len(R) % 2 == 0 or list(R[-(K - 1):]) != vals[-(K - 1):]: return task, 'TOUCH', None
                if M <= N: return task, 'NGROW', (vals, N, M)
                P2 = tuple(cls(x) for x in R)
                succ.add((r2, M % 2, P2))
        return task, 'OK', succ
    except Exception as e:
        return task, type(e).__name__, str(e)[:200]

inv3.work = work

if __name__ == '__main__':
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    confs = pickle.load(open('/tmp/an83/coinconfs.pkl', 'rb'))
    F = set()
    for r, par, runs in confs:
        a = [cls(x) for x in runs]
        if len(a) % 2 == 0: a = a[:-1]
        F.update(windows(r, par, a[:-2]))
    for l in open('/tmp/an83/orb83.txt'):
        p = l.split()
        if not p[0].isdigit(): continue
        a = [cls(int(x[1:])) for x in p[4:]]
        F.update(windows(int(p[3]), int(p[2]) % 2, a[:-2]))
    print('initial F', len(F), flush=True)
    CACHE = {}
    for rd in range(rounds):
        t0 = time.time()
        stats, missing, fails = inv3.check(F, CACHE, maxlen=int(os.environ.get('MAXLEN', '19')))
        print('ROUND', rd, 'F', len(F), 'stats', dict(stats), 'missing', len(missing), 'fails', len(fails),
              '%.0fs' % (time.time() - t0), flush=True)
        kinds = Counter(f[1] for f in fails)
        print('   fail kinds', dict(kinds), flush=True)
        for f in [f for f in fails if f[1] == 'HALT'][:10]: print('   HALT', f, flush=True)
        for f in [f for f in fails if f[1] not in ('HALT',)][:8]: print('   ', f, flush=True)
        pickle.dump((F, missing, fails, CACHE), open('/tmp/an83/inv4h_round.pkl', 'wb'))
        if kinds.get('HALT'): print('HALT inside the language', flush=True); break
        if not missing and not fails: print('CLOSED (heuristic)', flush=True); break
        F |= set(missing)
