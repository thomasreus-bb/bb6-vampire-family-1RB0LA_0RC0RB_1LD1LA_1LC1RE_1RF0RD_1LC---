"""Small symbolic Turing-machine simulator with shift rules (exact, no heuristics).

Tape side = list of segments, nearest first.  Segment = (word, exp): the word repeated exp times; the word is
written in spatial order *away from the head* (for the left side: word[0] is the cell nearest to the head).
exp is a Lin: constant + sum coef*var with var >= 0, coef >= 0.  The special segment REST (an unknown part of
the tape) may never be read; reading it raises Touched.  ZEROS = 0^infinity.
Head convention: config (L, q, R, d): the head is on the nearest cell of side d ('R' or 'L').
"""
from collections import namedtuple

class Touched(Exception): pass
class NeedSplit(Exception): pass
class Halt(Exception): pass

class Lin:
    __slots__ = ('c', 'v')
    def __init__(self, c=0, v=None):
        self.c = c; self.v = {k: x for k, x in (v or {}).items() if x}
    def __add__(s, o):
        if isinstance(o, int): return Lin(s.c + o, s.v)
        v = dict(s.v)
        for k, x in o.v.items(): v[k] = v.get(k, 0) + x
        return Lin(s.c + o.c, v)
    def __sub__(s, o):
        if isinstance(o, int): return Lin(s.c - o, s.v)
        v = dict(s.v)
        for k, x in o.v.items(): v[k] = v.get(k, 0) - x
        return Lin(s.c - o.c, v)
    def __mul__(s, k): return Lin(s.c * k, {a: b * k for a, b in s.v.items()})
    def sym(s): return bool(s.v)
    def __eq__(s, o):
        if isinstance(o, int): o = Lin(o)
        if not isinstance(o, Lin): return False
        return s.c == o.c and s.v == o.v
    def __hash__(s): return hash((s.c, tuple(sorted(s.v.items()))))
    def __repr__(s):
        t = ['%s%s' % ('' if x == 1 else x, k) for k, x in sorted(s.v.items())]
        if s.c or not t: t.append(str(s.c))
        return '+'.join(t)
    def nonneg(s): return s.c >= 0 and all(x >= 0 for x in s.v.values())
def L(c=0, **v): return Lin(c, v)
REST = ('REST', None)
ZEROS = ('0', 'inf')

def parse_tm(tm):
    T = {}
    for i, g in enumerate(tm.split('_')):
        for b in (0, 1):
            x = g[3 * b:3 * b + 3]
            T[(chr(65 + i), str(b))] = None if x[0] == '-' else (x[0], x[1], x[2])
    return T

def norm(side):
    """merge equal neighbours, drop empty segments"""
    out = []
    for w, e in side:
        if not isinstance(e, (Lin, int)):
            if (w, e) == ZEROS:
                while out and out[-1][0] == '0' and isinstance(out[-1][1], Lin): out.pop()
            out.append((w, e)); continue
        if isinstance(e, int): e = Lin(e)
        if len(w) > 1 and len(set(w)) == 1:
            e = e * len(w); w = w[0]
        if e == 0: continue
        if not e.nonneg(): raise ValueError('negative exponent %r' % (e,))
        if out and out[-1][0] == w and isinstance(out[-1][1], Lin):
            out[-1] = (w, out[-1][1] + e)
        else:
            out.append((w, e))
    return out

def pop_cell(side):
    """remove and return the nearest cell of a side (list is modified)."""
    w, e = side[0]
    if w == 'REST': raise Touched()
    if e == 'inf': return '0'
    if e.c >= 1:
        rest = e - 1
        side[0:1] = [(c, Lin(1)) for c in w[1:]] + ([(w, rest)] if not rest == 0 else [])
        # put the first char back as consumed
        return w[0]
    raise NeedSplit((w, e))

def push(side, c):
    side.insert(0, (c, Lin(1)))

class Sim:
    def __init__(self, tm):
        self.T = parse_tm(tm)
        self.steps = 0
    def shift(self, q, word, d):
        """try a shift rule: state q facing side d enters one copy of word (spatial order away from head).
        returns written word (spatial order away from head on the *other* side, i.e. nearest first) or None."""
        cells = list(word); n = len(cells)
        # position i = index of the cell the head is on, counted from the near end; head starts on cells[0]
        i = 0; st = q; written = {}
        tape = cells[:]
        for _ in range(200 * n + 50):
            c = tape[i]
            t = self.T[(st, c)]
            if t is None: return None
            w, m, st = t
            tape[i] = w
            forward = (m == d)          # moving away from the head's origin side into the word
            i = i + 1 if forward else i - 1
            if i < 0: return None       # left the window backwards
            if i == n:
                if st != q: return None
                return tape             # cells now behind the head, in spatial order away from... see apply
        return None
    def shift2(self, q, c, u, d, K=6):
        """head (state q) on a cell c followed by u^e (direction d). Try: c u^K -> v c u^(K-1) with the rest
        untouched and the head never leaving the window. returns v (spatial order away from the old head side)."""
        n = len(u); win = [c] + list(u) * K; tape = win[:]; i = 0; st = q; mx = 0
        for _ in range(400 * n + 100):
            t = self.T[(st, tape[i])]
            if t is None: return None
            w, m, st = t; tape[i] = w
            i = i + 1 if m == d else i - 1
            if i < 0 or i >= len(win) - 1: return None
            mx = max(mx, i)
            if i == n and st == q and tape[n] == c and tape[n+1:] == win[n+1:]:
                return tape[:n]
        return None
    def run(self, cfg, maxsteps, stop=None):
        Ls, q, Rs, d = cfg
        Ls = list(Ls); Rs = list(Rs)
        for _ in range(maxsteps):
            if stop and stop(Ls, q, Rs, d): return (Ls, q, Rs, d)
            front = Rs if d == 'R' else Ls
            back = Ls if d == 'R' else Rs
            w0, e0 = front[0]
            if isinstance(e0, Lin) and e0.sym():
                wr = self.shift(q, w0, d)
                if wr is not None:
                    front.pop(0)
                    # head passed through the whole block; cells behind it in order nearest-first are reversed(wr)
                    back.insert(0, (''.join(reversed(wr)), e0))
                    nb = norm(back); back[:] = nb
                    continue
            done = False
            if (len(front) > 1 and isinstance(e0, Lin) and e0 == 1 and len(w0) == 1
                    and isinstance(front[1][1], Lin) and front[1][1].sym()):
                u0, e1 = front[1]
                for p in (1, 2, 3, 4):
                    if any(x % p for x in e1.v.values()): continue
                    ep = Lin(e1.c // p, {k: x // p for k, x in e1.v.items()}); rem = e1.c % p
                    if ep.c < 6: continue
                    u = u0 * p
                    v = self.shift2(q, w0, u, d)
                    if v is None: continue
                    front[0:2] = [(w0, Lin(1)), (u, Lin(6))] + ([(u0, Lin(rem))] if rem else [])
                    back.insert(0, (''.join(reversed(v)), ep - 6))
                    nb = norm(back); back[:] = nb; nf = norm(front); front[:] = nf
                    done = True; break
            if done: continue
            c = pop_cell(front)
            t = self.T[(q, c)]
            if t is None: raise Halt((Ls, q, Rs, d, c))
            w, m, q = t
            self.steps += 1
            if m == d:
                push(back, w)
            else:
                push(front, w)
                d = m
            Ls[:4] = norm(Ls[:4]) if len(Ls) > 4 else norm(Ls)
            Rs[:4] = norm(Rs[:4]) if len(Rs) > 4 else norm(Rs)
        raise RuntimeError('maxsteps')
