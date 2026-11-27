"""exact orbit at event level with on-the-fly learned affine rules.
key=(q,W,u,S); rule: for n = r mod m: next key, n' = a n + b (Fractions). Learned from synthetic runs with n ~ N0."""
import sys, fractions, functools, time, json
sys.path.insert(0,'/tmp/an'); import learn, evstep
class Orbit:
    def __init__(s,TM,evs,N0=300,reps=3,mods=(1,2,3,4,6,8,12,16,24,32,48,64,96)):
        s.TM=TM; s.evs=evs; s.N0=N0; s.reps=reps; s.mods=mods; s.rules={}; s.calls=0
    @functools.lru_cache(maxsize=None)
    def ev(s,q,W,u,n,S):
        s.calls+=1
        r=evstep.evrun(s.TM,q,W+u*n+S,s.evs)
        if r[0]=='HALT': return ('HALT',)
        if len(r)<3: return (r[0],)
        q2,st,t=r; p=learn.parse(t)
        if p is None: return ('NOPARSE',)
        return (q2,p[0],p[1],p[2],p[3],st)
    def fit(s,key):
        q,W,u,S=key
        N0=max(s.N0,4*(len(W)+len(S))+60)
        for m in s.mods:
            tab={}; ok=True
            for r in range(m):
                pts=[]
                for k in range(s.reps):
                    n=N0+((r-N0)%m)+m*k
                    pts.append((n,s.ev(q,W,u,n,S)))
                kinds={(x[1][0],) if len(x[1])<5 else (x[1][0],x[1][1],x[1][2],x[1][4]) for x in pts}
                if len(kinds)!=1: ok=False;break
                e=pts[0][1]
                if len(e)<5: tab[r]=(e[0],); continue
                a=fractions.Fraction(pts[1][1][3]-pts[0][1][3],pts[1][0]-pts[0][0]); b=pts[0][1][3]-a*pts[0][0]
                if any(a*x+b!=y[3] for x,y in pts): ok=False;break
                tab[r]=((e[0],e[1],e[2],e[4]),a,b)
            if ok: return m,tab
        return None
    def rule(s,key):
        if key not in s.rules: s.rules[key]=s.fit(key)
        return s.rules[key]
    def step(s,key,n):
        f=s.rule(key)
        if f is None: return 'NOFIT',None
        m,tab=f; e=tab[n%m]
        if len(e)==1: return e[0],None
        k2,a,b=e; n2=a*n+b
        assert n2.denominator==1
        return k2,int(n2)
