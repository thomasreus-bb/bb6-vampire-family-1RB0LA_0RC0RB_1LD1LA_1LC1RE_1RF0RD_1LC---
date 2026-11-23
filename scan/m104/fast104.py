"""fast104.py - Bell-level simulator for candidate 104 with big integers.

Same map as dm104.py / sim104.c (DeepMind section 2.5), stack stored
run-length encoded (top at the list end), plus the Bell acceleration
    (d odd, [3, 0^c, ...]) -> (d + 6m, [3, 0^(c-2m), ...]).
Each acceleration is one Bell; between Bells only a few dozen macro
steps run.  d grows by a factor of about 3/2 per Bell.

Usage: python3 fast104.py [bells] [every]
Prints per report: Bell, macro steps (log10), log10 d, stack length
(log10), number of even entries, number of runs, max scan depth.
"""
import sys, math

def run(maxbells, every=1, out=print, verbose=True):
    V = [0]; C = [1]           # runs, top at end
    st = {'len': 1, 'even': 1}
    def push(v, c):
        if c <= 0: return
        st['len'] += c
        if v % 2 == 0: st['even'] += c
        if V and V[-1] == v: C[-1] += c
        else: V.append(v); C.append(c)
    def pop():
        v = V[-1]; C[-1] -= 1
        if C[-1] == 0: V.pop(); C.pop()
        st['len'] -= 1
        if v % 2 == 0: st['even'] -= 1
        return v
    def drain(ks, hi, d):
        while True:
            if hi == 0: return d + 2
            if hi == 1: push(d + 1, 1); push(0, ks[0]); return 1
            j1, j2 = ks[hi-1], ks[hi-2]; hi -= 2
            if j1 == 0: d = 2*j2 + d + 6
            else: push(d + 1, 1); push(0, j1 - 1); d = 2*j2 + 5
    d = 0; steps = 0; bells = 0; maxscan = 0; hist = []
    while bells < maxbells:
        if d % 2 and len(V) >= 2 and V[-1] == 3 and C[-1] == 1 and V[-2] == 0 and C[-2] >= 4:
            m = (C[-2] - 2) // 2
            C[-2] -= 2*m; st['len'] -= 2*m; st['even'] -= 2*m; d += 6*m; steps += m
            bells += 1
            rec = (bells, steps, d, st['len'], st['even'], len(V), maxscan)
            hist.append(rec[:1] + (d % 8,) + rec[3:])
            if verbose and bells % every == 0:
                out("bell %d log10steps %.2f log10d %.2f log10len %.2f even %d runs %d maxscan %d" % (
                    bells, math.log10(steps), math.log10(d), math.log10(st['len']),
                    st['even'], len(V), maxscan))
            maxscan = 0
            continue
        steps += 1; ks = []; depth = 0
        while True:
            if st['len'] == 0:
                if d % 2:
                    out("HALT at macro step %d (Bell %d)" % (steps, bells)); return hist, True
                if not ks: push(0, d//2 + 1); d = 1
                else:
                    k0 = ks.pop(); push(0, d//2); d = drain(ks, len(ks), 2*k0 + 5)
                break
            e = pop(); depth += 1
            if d % 2: ks.append(d // 2); d = e
            else: d = drain(ks, len(ks), d + e + 2); break
        maxscan = max(maxscan, depth)
    return hist, False

if __name__ == '__main__':
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    ev = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    run(nb, ev, out=lambda s: (print(s), sys.stdout.flush()))
