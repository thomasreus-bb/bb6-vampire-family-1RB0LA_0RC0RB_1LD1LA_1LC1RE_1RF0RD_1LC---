#!/usr/bin/env python3
"""Run-length chain simulator for a 2-symbol TM (bbchallenge notation).
Each side of the head: runs (outward-ordered word, count) + a small buffer (outward order).
Chain step: a whole run w^c is crossed at once if crossing one copy of w returns the head
in the same state on the far side."""
import sys

PERIODS = (14, 7, 4, 2, 1)

def compress(s):
    out = []; i = 0; n = len(s)
    while i < n:
        best = None
        for q in (1, 2, 3, 4, 7, 14):
            if i + 2*q > n: continue
            w = s[i:i+q]; c = 1
            while s[i+c*q:i+(c+1)*q] == w: c += 1
            need = 3 if q == 1 else 2
            if c >= need and (best is None or c*q > best[0]*len(best[1])):
                best = (c, w)
        if best:
            c, w = best; out.append([w, c]); i += c*len(w)
        else:
            out.append([s[i], 1]); i += 1
    return out

class Side:
    __slots__ = ('runs', 'buf')
    def __init__(self):
        self.runs = []      # list of [word(str, outward order), count]; last = nearest head
        self.buf = ''       # outward order: buf[0] nearest head

def parse(M):
    T = []
    for st in M.split('_'):
        row = []
        for b in range(2):
            x = st[3*b:3*b+3]
            row.append(None if x[2] == '-' else (int(x[0]), 1 if x[1] == 'R' else -1, ord(x[2]) - 65))
        T.append(row)
    return T

class Sim:
    def __init__(self, M):
        self.T = parse(M)
        self.side = {1: Side(), -1: Side()}   # 1 = right side, -1 = left side
        self.s = 0; self.d = 1; self.steps = 0; self.pos = 0
        self.lo = 0; self.hi = 0
        self.cache = {}
        self.halted = False

    def fold(self, sd):
        b = sd.buf
        runs = sd.runs
        changed = True
        while changed and b:
            changed = False
            if runs:
                w, c = runs[-1]
                q = len(w)
                if len(b) >= q and b[-q:] == w:
                    runs[-1][1] += 1; b = b[:-q]; changed = True; continue
            for q in PERIODS:
                if len(b) >= 2*q and b[-q:] == b[-2*q:-q]:
                    runs.append([b[-q:], 2]); b = b[:-2*q]; changed = True; break
        if len(b) > 40:
            # move the farthest cells to runs, re-compressing them together with small top runs
            chunk = b[28:]; b = b[:28]
            S = chunk; tot = 0
            while runs and len(runs[-1][0])*runs[-1][1] <= 60 and tot < 240:
                w, c = runs.pop(); S += w*c; tot += len(w)*c
            comp = compress(S)
            for w, c in reversed(comp):
                if runs and runs[-1][0] == w: runs[-1][1] += c
                else: runs.append([w, c])
        sd.buf = b
        # re-compress many small runs at the top of the stack (aligned from the far side)
        k = 0; tot = 0
        while k < len(runs) and len(runs[-1-k][0])*runs[-1-k][1] <= 14 and tot < 240:
            tot += len(runs[-1-k][0])*runs[-1-k][1]; k += 1
        if k >= 10:
            S = ''.join(w*c for w, c in reversed(runs[-k:]))  # nearest first (outward order)
            del runs[-k:]
            comp = compress(S[::-1])                            # farthest first, inward words
            for w, c in comp:
                w = w[::-1]
                if runs and runs[-1][0] == w: runs[-1][1] += c
                else: runs.append([w, c])

    def flush(self, sd):
        self.fold(sd)
        b = sd.buf
        while b:
            cell = b[-1]; b = b[:-1]
            if sd.runs and sd.runs[-1][0] == cell: sd.runs[-1][1] += 1
            else: sd.runs.append([cell, 1])
        sd.buf = ''

    def read(self, sd):
        if not sd.buf:
            if not sd.runs:
                return '0'
            r = sd.runs[-1]
            r[1] -= 1
            if r[1] == 0: sd.runs.pop()
            sd.buf = r[0]
        c = sd.buf[0]; sd.buf = sd.buf[1:]
        return c

    def cross(self, s, w, d):
        """head in state s enters actual word w (left-to-right cells) from the side opposite to d.
        returns (state, word', steps) if it leaves on the far side, else None"""
        key = (s, w, d)
        if key in self.cache: return self.cache[key]
        t = list(w); n = len(t); p = 0 if d == 1 else n - 1; st = s; k = 0
        res = None
        while k < 10000:
            tr = self.T[st][int(t[p])]
            if tr is None: break
            t[p] = str(tr[0]); p += tr[1]; st = tr[2]; k += 1
            if p >= n:
                res = (st, ''.join(t), k) if d == 1 and st == s else None; break
            if p < 0:
                res = (st, ''.join(t), k) if d == -1 and st == s else None; break
        self.cache[key] = res
        return res

    def push_run(self, od, ow, c):
        cc = c
        for q in range(1, len(ow)):
            if len(ow) % q == 0 and ow[:q]*(len(ow)//q) == ow:
                cc = c*(len(ow)//q); ow = ow[:q]; break
        if od.runs and od.runs[-1][0] == ow: od.runs[-1][1] += cc
        else: od.runs.append([ow, cc])

    def peek(self, sd, k):
        """nearest k cells of a side in outward order (zeros beyond the tape)"""
        out = sd.buf[:k]
        i = len(sd.runs) - 1
        while len(out) < k and i >= 0:
            w, c = sd.runs[i]
            need = k - len(out)
            rep = min(c, need // len(w) + 1)
            out += (w * rep)[:need]
            i -= 1
        return out + '0' * (k - len(out))

    def drop(self, sd, k):
        for _ in range(k): self.read(sd)

    def cross_back(self, s, w, b, d):
        """backsymbol chain: w = actual word ahead, b = actual k cells behind the head.
        returns (deposit b' in actual order, steps) if after crossing w the head is beyond w
        in state s with the same backsymbol b."""
        key = ('B', s, w, b, d)
        if key in self.cache: return self.cache[key]
        n = len(w); k = len(b); res = None
        if d == -1: t = list(w + b); p = n - 1
        else: t = list(b + w); p = k
        st = s; steps = 0; N = n + k
        while steps < 20000:
            tr = self.T[st][int(t[p])]
            if tr is None: break
            t[p] = str(tr[0]); p += tr[1]; st = tr[2]; steps += 1
            if d == -1:
                if p < 0:
                    tt = ''.join(t)
                    if st == s and tt[:k] == b: res = (tt[k:], steps)
                    break
                if p >= N: break
            else:
                if p >= N:
                    tt = ''.join(t)
                    if st == s and tt[N-k:] == b: res = (tt[:N-k], steps)
                    break
                if p < 0: break
        self.cache[key] = res
        return res

    def step(self):
        d = self.d; sd = self.side[d]; od = self.side[-d]
        if not sd.buf and sd.runs and sd.runs[-1][1] >= 2:
            w0, c0 = sd.runs[-1]
            for mult in (1, 2, 3, 4):
                if c0 < 2*mult: break
                w = w0*mult; c = c0 // mult; rem = c0 - c*mult
                actual = w if d == 1 else w[::-1]
                r = self.cross(self.s, actual, d)
                if r is not None:
                    _, w2, k = r
                    if rem: sd.runs[-1][1] = rem
                    else: sd.runs.pop()
                    self.flush(od)
                    ow = w2 if d == -1 else w2[::-1]
                    self.push_run(od, ow, c)
                    self.steps += k * c
                    self.pos += d * len(w) * c
                    return
                kb = len(w)
                bo = self.peek(od, kb)                  # outward order on the other side
                bact = bo[::-1] if d == -1 else bo      # actual order: for d=-1 other side is right -> outward = actual
                bact = bo if d == -1 else bo[::-1]
                r = self.cross_back(self.s, actual, bact, d)
                if r is not None:
                    dep, k = r                          # actual order, len(w) cells... deposited behind b
                    if rem: sd.runs[-1][1] = rem
                    else: sd.runs.pop()
                    self.drop(od, kb)
                    self.flush(od)
                    # deposit c copies (outward order on od), then b nearest
                    if d == -1:
                        # other side = right; deposit lies right of b: outward order = actual
                        self.push_run(od, dep, c)
                        od.buf = bact
                    else:
                        self.push_run(od, dep[::-1], c)
                        od.buf = bact[::-1]
                    self.steps += k * c
                    self.pos += d * len(w) * c
                    return
        cell = self.read(sd)
        tr = self.T[self.s][int(cell)]
        if tr is None:
            sd.buf = cell + sd.buf; self.halted = True; return
        wv, mv, ns = tr
        # written cell goes to the side opposite to the move
        tgt = self.side[-mv]
        tgt.buf = str(wv) + tgt.buf
        self.fold(tgt)
        self.s = ns; self.d = mv; self.steps += 1
        self.pos += mv
        if self.pos > self.hi: self.hi = self.pos
        if self.pos < self.lo: self.lo = self.pos

    def tape(self):
        """full tape string left-to-right and head index"""
        L = self.side[-1]; R = self.side[1]
        left = ''.join(w * c for w, c in L.runs) [::-1]  # runs outward order: first = farthest? no
        # runs list: index 0 = farthest from head, last = nearest; words in outward order
        left = ''.join((w * c)[::-1] for w, c in L.runs) + L.buf[::-1]
        right = R.buf + ''.join((w * c) for w, c in reversed(R.runs))
        return left, right

if __name__ == '__main__':
    M = sys.argv[1]; N = int(sys.argv[2])
    S = Sim(M)
    for _ in range(N): S.step()
    l, r = S.tape()
    print(S.steps, S.s, S.d, len(l), len(r))
