import subprocess, sys, re, functools, fractions, itertools, json
TM=None
def runs(t):
    out=[];i=0
    while i<len(t):
        j=i
        while j<len(t) and t[j]==t[i]: j+=1
        out.append((t[i],j-i)); i=j
    return out
def parse(t, P=(1,2,3,4,5,6), minrep=6):
    best=None
    for p in P:
        i=0; L=len(t)
        while i+p<L:
            if t[i]==t[i+p]:
                j=i
                while j+p<L and t[j]==t[j+p]: j+=1
                n=(j+p-i)//p
                if n>=minrep and (best is None or n*p>best[1]*len(best[0]) ):
                    best=(t[i:i+p],n,i)
                i=j+1
            else: i+=1
    if not best: return None
    u,n,s=best
    # canonical: take smallest period that also works, normalize phase so that unit is lexicographically smallest rotation?  keep leftmost start
    return (t[:s],u,n,t[s+n*len(u):])
def run(q,tape,mx=10**9):
    r=subprocess.run(['/tmp/an/synth',TM,q,'0',str(mx)],input=tape+'\n',capture_output=True,text=True).stdout.split()
    if r[0]=='HALT': return ('HALT',int(r[2]))
    if r[0]=='REC': return (r[1],int(r[2]),r[3])
    return (r[0],)
@functools.lru_cache(maxsize=None)
def step(q,W,u,n,S):
    r=run(q,W+u*n+S)
    if r[0]=='HALT': return ('HALT',r[1])
    if len(r)<3: return (r[0],)
    q2,st,t=r; pr=parse(t)
    if pr is None: return ('NOPARSE',t[:80])
    W2,u2,n2,S2=pr
    return (q2,W2,u2,n2,S2,st)
def fit(q,W,u,S,mods=(1,2,3,4,6,8,12,16,24),n0=40,reps=4):
    for m in mods:
        ok=True; table={}
        for r in range(m):
            pts=[]
            for k in range(reps):
                n=n0+r+m*k
                while n<n0: n+=m
                res=step(q,W,u,n,S)
                pts.append((n,res))
            kinds=set((x[1][0],) if x[1][0] in ('HALT','NOPARSE','MAX','TAPE') else (x[1][0],x[1][1],x[1][2],x[1][4]) for x in pts)
            if len(kinds)!=1: ok=False;break
            kd=pts[0][1]
            if kd[0] in ('HALT','NOPARSE','MAX','TAPE'):
                table[r]=(kd[0],); continue
            ns=[(x[0],x[1][3]) for x in pts]
            a=fractions.Fraction(ns[1][1]-ns[0][1],ns[1][0]-ns[0][0]); b=ns[0][1]-a*ns[0][0]
            if any(a*x+b!=y for x,y in ns): ok=False;break
            table[r]=(kd[0],kd[1],kd[2],kd[4],a,b)
        if ok: return m,table
    return None
