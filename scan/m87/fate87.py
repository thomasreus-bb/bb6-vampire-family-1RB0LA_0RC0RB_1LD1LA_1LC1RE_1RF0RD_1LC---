# no. 87, with the DeepMind map (dm87.py): outcome distribution of a scan (Q, S4, S6 with large n) and the chance that the
# machine ends in HALT or in the endless R1 loop (R1(n) -> R1(n+5) forever = nonhalting).
import random,collections,sys
from fractions import Fraction as F
from dm87 import T
sys.set_int_max_str_digits(0)
random.seed(1)
out={H:collections.Counter() for H in ('Q','S4','S6')}
N=int(sys.argv[1]) if len(sys.argv)>1 else 300
for H in out:
    for _ in range(N):
        n=random.randint(1500,3000)
        r=T((H,n))
        out[H]['HALT' if r=='HALT' else r[0]]+=1
for H in out: print('scan',H,dict(out[H]))
# absorbing chain: states R2, Q, S4, S6 ; absorbing R1 (nonhalt) and HALT; R2: R1 2/5, R2 2/5, Q 1/5
P={'R2':{'R1':F(2,5),'R2':F(2,5),'Q':F(1,5)}}
for H in out:
    tot=sum(out[H].values()); P[H]={k:F(v,tot) for k,v in out[H].items()}
# solve h(s) = P(HALT eventually | s) by iteration
h={s:0.0 for s in P}; h['HALT']=1.0; h['R1']=0.0
for _ in range(2000):
    for s in P: h[s]=sum(float(p)*h[t] for t,p in P[s].items())
for s in ('S6','Q','S4','R2'): print('P(HALT eventually | %s) = %.3f'%(s,h[s]))
