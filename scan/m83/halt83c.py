import sys,random; sys.path.insert(0,'/tmp/an83')
from sym import Lin,L,Halt
import symbell
from functools import lru_cache
@lru_cache(maxsize=None)
def stepc(r,c0,S):
    try:
        M,r2,out=symbell.symbell(L(c0,n=4),r,[Lin(x) for x in S])
    except Halt: return 'HALT'
    except Exception as e: return 'ERR'
    o=[e.c for w,e in out]
    if len(o)%2==0: o=o[:-1]
    pars=(0,1) if any(x%2 for x in M.v.values()) else (M.c%2,)
    return (r2,pars,tuple(o))
def prob(r,par,S,D,cut=14):
    """probability of HALT within D Bells, N residues uniform"""
    if D==0: return 0.0
    S=tuple(S[:cut]) if len(S)>cut else tuple(S)
    if len(S)%2==0: S=S[:-1]
    tot=0.0; c0s=(101,103) if par else (100,102)
    for c0 in c0s:
        res=stepc(r,c0,S+(40,6,40,6))
        if res=='HALT': tot+=1/len(c0s); continue
        if res=='ERR': continue
        r2,pars,o=res
        o=o[:-4] if len(o)>4 else o
        for p2 in pars: tot+=prob(r2,p2,o,D-1,cut)/len(c0s)/len(pars)
    return tot
if __name__=='__main__':
    D=int(sys.argv[1])
    Lr=[l.split() for l in open('/tmp/an83/orb83.txt') if l.split()[0].isdigit()]
    for k in (1070,1074,1078):
        p=Lr[k]; r=int(p[3]); S=[int(x[1:]) for x in p[4:]]
        print(k,r,S[:7],'P(HALT within %d Bells)=%.4g'%(D,prob(r,1,S,D)),'cache',stepc.cache_info().currsize,flush=True)
