# Tails of the grammar X*Y that HALT for a large main counter n (residue 1), and where they lie.
#   gcc -O2 -o dstep dstep.c && gcc -O2 -o gmap2 ../m105/gmap2.c && python3 halting_tails.py
# P_j = 3.5.2^j.  All runs use M = mirrored A, start (110)^n W in state D with the head left of the tape.
import subprocess,os,collections
HERE=os.path.dirname(os.path.abspath(__file__))
M='1LB1RF_1RC1LD_1LA1RA_0LA0LE_0LC---_1LF0RC'
def word(t): return '0'.join('1'*k for k in t)
def P(j): return [3,5]+[2]*j
def gmap(n,W): return subprocess.run([os.path.join(HERE,'gmap2'),M,'D','-','110','110'*n+word(W),'20000000000','2'],capture_output=True,text=True).stdout.split()[0]
def halts_within(tapes,k):
    """True for the tapes that HALT within k left-edge steps (2 steps = one level)"""
    cur=list(enumerate(tapes)); res=[False]*len(tapes)
    for it in range(k):
        o=subprocess.run([os.path.join(HERE,'dstep'),'step'],input=''.join(' '.join(map(str,t))+'\n' for _,t in cur),capture_output=True,text=True).stdout.split('\n')
        nxt=[]
        for (i,t),l in zip(cur,o):
            f=l.split()
            if f[0]=='HALT': res[i]=True
            elif f[0]=='D': nxt.append((i,list(map(int,f[1:]))))
        cur=nxt
    return res
if __name__=='__main__':
    print('1. three blocks P_a P_b P_c and end 3, n = 41: all a < 7, b < 25, c < 90')
    keys=[(a,b,c) for a in range(7) for b in range(25) for c in range(90)]
    H=[k for k,h in zip(keys,halts_within([[2]*41+P(a)+P(b)+P(c)+[3] for a,b,c in keys],2)) if h]
    print('   %d of %d HALT: %s'%(len(H),len(keys),H))
    print('   all of them have b = 3a + 6 and c = 9a + 23 or 9a + 24:',all(b==3*a+6 and c in (9*a+23,9*a+24) for a,b,c in H))
    print('2. the same tails for other n (gmap2):')
    for a,b,c in ((2,12,41),(4,18,59)):
        ns=list(range(5,40))+[60,61,150,151]
        r={n:gmap(n,P(a)+P(b)+P(c)+[3]) for n in ns}
        print('   tail 3.5.2^%d.3.5.2^%d.3.5.2^%d.3: HALT for all odd n tested: %s; for no even n: %s'%(a,b,c,all(r[n]=='HALT' for n in ns if n%2),all(r[n]!='HALT' for n in ns if n%2==0)))
    print('3. two blocks P_a P_b and end 3, all n < 25, a < 25, b < 100, followed for 3 levels')
    keys=[(n,a,b) for n in range(25) for a in range(25) for b in range(100)]
    H=[k for k,h in zip(keys,halts_within([[2]*n+P(a)+P(b)+[3] for n,a,b in keys],6)) if h]
    print('   %d of %d HALT: %s'%(len(H),len(keys),H))
