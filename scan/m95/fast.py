#!/usr/bin/env python3
"""Fast simulation for Bell machines: chain simulator + canonical run-length form at
'left events' (state Q0, head at the blank left end, moving left) + extrapolation of
repeating event cycles (same run signature, constant count differences over two periods).
Usage: fast.py TM maxevents [T] """
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chain import Sim, Side

PER = (1, 2, 3, 4, 7, 14)

def compress(s):
    """greedy run-length compression of a cell string into [word,count] runs (left to right)"""
    out = []; i = 0; n = len(s)
    while i < n:
        best = None
        for q in PER:
            if i + 2*q > n: continue
            w = s[i:i+q]; c = 1
            while s[i+c*q:i+(c+1)*q] == w: c += 1
            need = 3 if q == 1 else 2
            if c >= need and (best is None or c*q > best[0]*len(best[1])):
                best = (c, w)
        if best:
            c, w = best
            out.append([w, c]); i += c*len(w)
        else:
            out.append([s[i], 1]); i += 1
    return out

def merge(runs):
    """merge adjacent equal words; returns list"""
    res = []
    for w, c in runs:
        if res and res[-1][0] == w: res[-1][1] += c
        else: res.append([w, c])
    return res

def canon_right(S, T, side=1):
    """head at one blank end: everything lies on the other side. Rebuild that side
    canonically (outward order); runs with count >= T stay, the rest is re-compressed."""
    R = S.side[side]
    segs = []  # left-to-right list of either [word,count] (big) or str (literal)
    if R.buf: segs.append(R.buf)
    for w, c in reversed(R.runs):
        for q in range(1, len(w)):
            if len(w) % q == 0 and w[:q]*(len(w)//q) == w:
                c = c*(len(w)//q); w = w[:q]; break
        if c >= T or len(w)*c > 60: segs.append([w, c])
        else: segs.append(w*c)
    # join literals
    out = []; lit = ''
    for x in segs:
        if isinstance(x, str): lit += x
        else:
            if lit: out += compress(lit); lit = ''
            out.append(x)
    if lit: out += compress(lit)
    # strip trailing zeros
    while out and set(out[-1][0]) == {'0'}: out.pop()
    out = merge(out)
    # absorb literal copies next to big runs (repeat until stable)
    changed = True
    while changed:
        changed = False
        for i in range(len(out)-1):
            a, b = out[i], out[i+1]
            if a[1] >= 2 and b[1] < T and len(b[0])*b[1] % len(a[0]) == 0 and b[0]*b[1] == a[0]*(len(b[0])*b[1]//len(a[0])):
                a[1] += len(b[0])*b[1]//len(a[0]); del out[i+1]; changed = True; break
            if b[1] >= 2 and a[1] < T and len(a[0])*a[1] % len(b[0]) == 0 and a[0]*a[1] == b[0]*(len(a[0])*a[1]//len(b[0])):
                b[1] += len(a[0])*a[1]//len(b[0]); del out[i]; changed = True; break
    R.buf = ''
    R.runs = [list(x) for x in reversed(out)]
    return out

def sig(out, T):
    return tuple((w, c if c < T else None) for w, c in out)

def run(M, maxev, T=9, report=None, verbose=False):
    S = Sim(M)
    hist = []   # (signature, counts, steps)
    ev = 0
    while ev < maxev and not S.halted:
        S.step()
        d = S.d; E = S.side[d]
        if not E.runs and '1' not in E.buf:
            E.buf = ''
            side = -d
            out = canon_right(S, T, side)
            ev += 1
            sg = (d, S.s, sig(out, T)); cnt = [c for w, c in out if c >= T]
            if report and d == -1 and S.s == 0: report(S, out)
            hist.append((sg, cnt, S.steps))
            if len(hist) > 160: hist.pop(0)
            for p in range(1, 61):
                if len(hist) < 2*p+1: break
                s0, c0, t0 = hist[-1-2*p]; s1, c1, t1 = hist[-1-p]; s2, c2, t2 = hist[-1]
                if not (s0 == s1 == s2): continue
                d1 = [b-a for a, b in zip(c0, c1)]; d2 = [b-a for a, b in zip(c1, c2)]
                if d1 != d2 or not any(d1): continue
                n = None
                for c, dl in zip(c2, d2):
                    if dl < 0:
                        k = (c - T - 2*(-dl)) // (-dl)
                        n = k if n is None else min(n, k)
                if n is None or n < 2: continue
                e1 = t1 - t0; e2 = t2 - t1; dd = e2 - e1
                S.steps += n*e2 + dd*n*(n+1)//2
                big = [x for x in reversed(S.side[side].runs) if x[1] >= T]
                for x, dl in zip(big, d2): x[1] += n*dl
                ev += n*p
                hist.clear()
                if verbose: print('  extrapolated', n, 'periods of', p, 'events', file=sys.stderr)
                break
    return S

if __name__ == '__main__':
    M = sys.argv[1]; N = int(sys.argv[2]); T = int(sys.argv[3]) if len(sys.argv) > 3 else 9
    def rep(S, out):
        pass
    S = run(M, N, T, verbose=True)
    print(S.steps, S.halted)
