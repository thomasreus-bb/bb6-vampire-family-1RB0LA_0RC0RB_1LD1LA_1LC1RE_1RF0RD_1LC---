# no. 65: cycle table and Markov chain. A cycle with B runs t = B div 4 steps of s (s0 = 2, s' = floor((3s+8)/2)),
# r = B mod 4 and a = s_t decide HALT or the next B (map65.py rules).
import collections,random
from map65 import step
def cycle_end(B,a):
    # returns next B or None (HALT), given a = s_t
    t,r=divmod(B,4); b=r
    s=(a,b)
    while True:
        s=step(*s)
        if s is None: return None
        if s[0]==2: return s[1]
# table: (r, a mod 8) -> next B mod 4 or HALT (independent of the higher bits; checked below)
tab={}
for r in range(4):
    for a8 in range(8):
        outs=set()
        for hi in range(0,400,8):
            a=a8+hi+8
            nb=cycle_end(4*10+r,a)
            outs.add('H' if nb is None else nb%4)
        tab[(r,a8)]=outs
print('table (r = B mod 4, a = s_t mod 8) -> next B mod 4 or HALT:')
for r in range(4): print('  r=%d:'%r,'  '.join('a≡%d:%s'%(a8,'/'.join(map(str,sorted(tab[(r,a8)],key=str)))) for a8 in range(8)))
# empirical check of uniform low bits of s_t
T=200000; s=2; low=[]
for i in range(T+1):
    low.append(s%8); s=(3*s+8)//2
c=collections.Counter(low[1000:]); print('s_t mod 8 for 1000<t<=%d:'%T,{k:round(v/(T-1000),4) for k,v in sorted(c.items())})
# Markov chain on r with uniform a mod 8
P={r:collections.Counter() for r in range(4)}
for (r,a8),o in tab.items():
    (x,)=o; P[r][x]+=1/8
print('transition probabilities:',{r:dict(P[r]) for r in P})
dist={2:1.0}; cum=0
for k in range(1,15):
    new=collections.Counter(); h=0
    for r,p in dist.items():
        for x,q in P[r].items():
            if x=='H': h+=p*q
            else: new[x]+=p*q
    cum+=h; dist=new
    print('cycle end %d (the current one is 1): P(HALT here) = %.4f, cumulative %.4f'%(k,h,cum))
    if 1-cum<1e-4: break
