"""Exact symbolic Bell step of no. 83 (mirrored TM), using sym.py.
Input: r, list of S runs (Lin or int), N = 4n + c0 (c0 in {101, 103}), tail REST.
Phases: (1) run from the Bell config until the first left record in state A with tape 0^inf A> [1^m, 0^z, ...]
with m an even constant >= 14 and z = 4*n*... ; (2) apply the slow-phase lemma SP k times (proved in sp83.py:
C_A(m, z+4) -> C_A(m+6, z) for even m >= 14, any z, rest untouched); (3) run to the next Bell config
(left record in state B, tape 1^M 0^r' 1...).  Returns ('BELL', M, r', S'), or raises Halt/Touched/..."""
import sys; sys.path.insert(0, '/tmp/an83')
from sym import *
TM = '1LB1LA_1RC0LB_1RD0RB_1LA0RE_---1RF_1RB0RA'

def bell_cfg(N, r, runs):
    R = [('1', N), ('0', Lin(r))]
    for i, x in enumerate(runs):
        R.append(('1' if i % 2 == 0 else '0', x if isinstance(x, Lin) else Lin(x)))
    R.append(REST)
    return ([ZEROS], 'B', norm(R), 'L')

class Fail(Exception): pass

def symbell(N, r, runs, maxsteps=400000):
    s = Sim(TM)
    cfg = bell_cfg(N, r, runs)
    cnt = [0]
    def isB(Ls, q, Rs, d):
        return (q == 'B' and d == 'L' and Ls == [ZEROS] and len(Rs) >= 2 and Rs[0][0] == '1' and Rs[0][1].sym()
                and Rs[1][0] == '0' and not Rs[1][1].sym() and 1 <= Rs[1][1].c <= 3)
    def isSP(Ls, q, Rs, d):
        if not (q == 'A' and d == 'L' and Ls == [ZEROS] and len(Rs) >= 3 and Rs[0][0] == '1' and Rs[1][0] == '0'):
            return False
        m, z = Rs[0][1], Rs[1][1]
        return (isinstance(m, Lin) and isinstance(z, Lin) and m.c >= 14 and m.c % 2 == 0
                and all(x % 2 == 0 for x in m.v.values()) and z.sym() and all(x % 4 == 0 for x in z.v.values()) and z.c >= 4)
    def stop(Ls, q, Rs, d):
        cnt[0] += 1
        return cnt[0] >= 3 and (isB(Ls, q, Rs, d) or isSP(Ls, q, Rs, d))
    Ls, q, Rs, d = cfg
    nsp = 0
    while True:
        cnt[0] = 0
        Ls, q, Rs, d = s.run((Ls, q, Rs, d), maxsteps, stop)
        if q == 'B': return finish(Rs)
        # slow-phase lemma SP applied k times: C_A(m, z) -> C_A(m + 6k, z - 4k)
        m, z = Rs[0][1], Rs[1][1]
        zkeep = 4 + (z.c % 4)
        k = Lin((z.c - zkeep) // 4, {a: x // 4 for a, x in z.v.items()})
        Rs = norm([('1', m + k * 6), ('0', Lin(zkeep))] + Rs[2:])
        nsp += 1
        if nsp > 20: raise Fail('too many SP')

def finish(Rs):
    M, r2 = Rs[0][1], Rs[1][1].c
    rest = Rs[2:]
    out = []
    for w, e in rest:
        if w == 'REST': break
        out.append((w, e))
    if not rest or rest[-1] != REST: raise Fail('noREST')
    return M, r2, out

if __name__ == '__main__':
    import subprocess
    # validation against cyc83 with concrete S and symbolic N
    for r, S in ((1, [14, 6, 12, 22, 10]), (3, [14, 6, 12, 22, 10]), (1, [8, 2, 12, 20, 6]), (3, [7, 2, 6, 8, 6])):
        for c0 in (101, 103):
            M, r2, out = symbell(L(c0, n=4), r, S)
            print(r, S, c0, '->', M, r2, out)
            for nv in (0, 3):
                N = c0 + 4 * nv
                Sw = ''.join(('1' if i % 2 == 0 else '0') * x for i, x in enumerate(S)) + '0' * 40 + '1' * 6
                o = subprocess.run(['/tmp/an83/cyc83', str(N), str(r), Sw, '100000000'], capture_output=True, text=True).stdout.split()
                print('    cyc83 N=%d' % N, o[:3], [len(x) for x in __import__('re').findall(r'0+|1+', o[3])][:8] if o[0] == 'BELL' else '')
