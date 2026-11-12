# exact macro step of no. 41 for all counter values: table for small values + affine continuation, with loop acceleration
import pickle
R=pickle.load(open('tab14.pkl','rb')); K=7   # affine beyond K in every coordinate (checked on the table up to 14)
def step(kind,p):
    """one macro step (first later macro configuration)"""
    q=tuple(min(x,K) for x in p)
    r=R[(kind,q)]
    if r[0] in('HALT','MAX'): return r[0],None
    out=list(r[1])
    for i,x in enumerate(p):
        if x>K:
            e=list(q); e[i]+=1; r2=R[(kind,tuple(e))]
            assert r2[0]==r[0],(kind,p)
            for j in range(len(out)): out[j]+=(x-K)*(r2[1][j]-r[1][j])
    return r[0],tuple(out)
def run(kind,p):
    """follow self-loops of constant shift in one jump; returns the next configuration of another kind (or after a changed rule)"""
    k2,p2=step(kind,p)
    if k2!=kind or p2 is None: return k2,p2
    d=tuple(y-x for x,y in zip(p,p2))
    # number of further rounds while all coordinates that decrease stay > K+|d|
    m=min(((x-K-1)//(-di) for x,di in zip(p2,d) if di<0),default=0)
    m=max(m,0)
    return kind,tuple(x+m*di for x,di in zip(p2,d))
def next_bell(n,maxit=10**7):
    kind,p=step('Bell',(n,)); it=0; trace=[]
    while kind!='Bell':
        if kind in('HALT','MAX'): return kind,it
        kind,p=run(kind,p); it+=1
        if it>maxit: return 'LOOP',it
    return p[0],it
if __name__=='__main__':
    # check 1: the affine continuation against the table itself (all entries with a coordinate > K)
    bad=0;tot=0
    for (kind,p),r in R.items():
        if max(p)>K:
            tot+=1; s=step(kind,p)
            if (s[0],s[1])!=(r[0],r[1] if r[0] not in('HALT','MAX') else None): bad+=1
    print('continuation vs table: %d entries, %d differ'%(tot,bad))
    n=8; seq=[n]
    for i in range(24):
        n,it=next_bell(n); seq.append(n)
        if not isinstance(n,int): break
    print(seq[:14]); print('Bell 25:',seq[-1])

def run2(kind,p):
    """like run, and also jumps over 2-cycles of kinds with a constant shift (phase A: A -> P2 -> A)"""
    k1,p1=run(kind,p)
    if p1 is None or k1==kind: return k1,p1
    k2,p2=step(k1,p1)
    if k2!=kind or p2 is None: return k1,p1
    k3,p3=step(k2,p2)
    if k3!=k1 or p3 is None: return k1,p1
    d=tuple(y-x for x,y in zip(p1,p3))
    k4,p4=step(k3,p3)
    if k4!=kind or tuple(y-x for x,y in zip(p2,p4))!=tuple(y-x for x,y in zip(p,p2)): return k1,p1
    m=min(((x-K-3)//(-di) for x,di in zip(p3,d) if di<0),default=0)
    if m<=0: return k1,p1
    return k1,tuple(x+m*di for x,di in zip(p3,d))
def cycle(n,maxit=10**6,rec=None):
    kind,p=step('Bell',(n,)); it=0
    while kind!='Bell':
        if kind in('HALT','MAX'): return kind,it
        if rec is not None: rec.append((kind,p))
        kind,p=run2(kind,p); it+=1
        if it>maxit: return 'LOOP',it
    return p[0],it
