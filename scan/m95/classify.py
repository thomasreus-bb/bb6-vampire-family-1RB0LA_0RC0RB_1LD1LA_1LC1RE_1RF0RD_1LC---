#!/usr/bin/env python3
"""Classify the Bell starts (B lines of fastbe.py) of no. 95:
left block (period-4 word) count a, middle counters (period-2 runs, merged across 1-cell gaps),
reservoir k (period-14 word). Type = number of middle counters: A=0, B=1, C=2, D=3 ..."""
import re, sys

def toks(s):
    out = []
    for t in s.split():
        m = re.fullmatch(r'\(([01]+)\)\^(\d+)', t)
        if m: out.append((m.group(1), int(m.group(2))))
        else: out.append((t, 1))
    return out

def analyse(s):
    T = toks(s)
    a = None; k = None; ctr = []
    us = [(c, i) for i, (w, c) in enumerate(T) if len(w) == 14 and c >= 2]
    i_u = max(us)[1]
    k = T[i_u][1]
    i_a = next((i for i, (w, c) in enumerate(T[:i_u]) if len(w) == 4 and c >= 9), None)
    a = T[i_a][1] if i_a is not None else 0
    start = (i_a + 1) if i_a is not None else 0
    # middle counters: period-2 runs between left block and reservoir; merge (10)^x 1 (01)^y etc.
    cur = None; gap = ''; lastw = None
    for w, c in T[start:i_u]:
        if len(w) == 2 and c >= 2:
            joint = (lastw[-1] if lastw else '') + gap + w[0]
            alt = all(joint[i] != joint[i+1] for i in range(len(joint)-1))
            if cur is not None and len(gap) <= 8 and alt:
                cur += c
            else:
                if cur is not None: ctr.append(cur)
                cur = c
            gap = ''; lastw = w
        else:
            gap += w * c
    if cur is not None: ctr.append(cur)
    ctr = [x for x in ctr if x >= 9]
    return a, ctr, k

if __name__ == '__main__':
    n = 0
    for line in open(sys.argv[1]):
        if not line.startswith('B '): continue
        _, steps, rest = line.split(' ', 2)
        try:
            a, ctr, k = analyse(rest)
        except (StopIteration, ValueError):
            print('??', steps, rest[:150]); continue
        n += 1
        typ = 'ABCDEFG'[len(ctr)]
        print(n, typ, steps, 'a=%d' % a, 'counters=%s' % ctr, 'k=%d' % k)
