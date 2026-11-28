"""Coin model for no. 83 with exact N parity: next N rep = small number with the same residue mod 8 as the
next 1-run M of the representative run (so forced parities/residues are kept, free ones are pseudo-random)."""
import subprocess, random, re, sys, time
from collections import Counter
P = 600
def runs(s): return [len(m.group(0)) for m in re.finditer(r'0+|1+', s)]
def chain(seed, NB, S0, r0):
    rnd = random.Random(seed); S = S0; r = r0; Nres = 1 + 2 * rnd.randrange(4)  # N mod 8
    st = Counter(); events = []; hist = []
    for k in range(NB):
        St = S[:P]
        St = St[:len(St) - (len(St) - len(St.rstrip('0')))]
        # cut at a block end
        while St and St[-1] == '1' and len(St) < len(S) and S[len(St)] == '1': St = St[:-1]; St = St.rstrip('1').rstrip('0') if False else St
        St = St.rstrip('0')
        base = int(__import__("os").environ.get("NB8","60")) + rnd.randrange(0, 20)
        N = 8 * base + Nres
        o = subprocess.run(['/tmp/an83/cyc83', str(N), str(r), St, '4000000000'], capture_output=True, text=True).stdout.split()
        if o[0] == 'HALT':
            st['HALT'] += 1; events.append(('HALT', k, r, N % 8, runs(St)[:9])); break
        if o[0] != 'BELL': st[o[0]] += 1; events.append((o[0], k, r, N % 8, runs(St)[:9])); break
        M = int(o[1]); r = int(o[2]); S2 = o[3]
        S = S2 + S[len(St):]
        Nres = M % 8
        R = runs(S[:300])
        hist.append((k, r, M % 2, R[:9])); hist = hist[-6:]
        st['bells'] += 1; st['par%d' % (M % 2)] += 1
        if any(R[i] == 1 for i in range(1, len(R), 2)):
            st['gap1'] += 1; ctx = tuple(R[:5]); st[('g1ctx', r, M % 2) + ctx] += 1
        if any(R[i] <= 5 for i in range(0, len(R) - 1, 2)): st['blk<=5'] += 1
        if R[0] <= 4: st['front<=4'] += 1; events.append(('front<=4', k, r, M % 2, R[:9]))
        if any(R[i] == 1 and R[i + 1] <= 5 for i in range(1, len(R) - 1, 2)): st['gap1+blk<=5'] += 1; events.append(('DANGER', k, r, M % 2, R[:9], list(hist)))
    return st, events
if __name__ == '__main__':
    from multiprocessing import Pool
    seeds = int(sys.argv[1]); NB = int(sys.argv[2])
    L = [l.split() for l in open('/tmp/an83/orb83.txt') if l.split()[0].isdigit()]
    S0 = ''.join(x[0] * int(x[1:]) for x in L[-1][4:]); r0 = int(L[-1][3])
    t = time.time()
    with Pool(2) as p: res = p.starmap(chain, [(s, NB, S0, r0) for s in range(seeds)])
    st = Counter(); ev = []
    for a, b in res: st += a; ev += b
    print(dict(st), '%.0fs' % (time.time() - t))
    for e in ev:
        if e[0] != 'front<=4': print(e)
    for k, v in sorted(st.items(), key=lambda kv: -kv[1] if isinstance(kv[0], tuple) else 0)[:40]:
        if isinstance(k, tuple): print(v, k)
