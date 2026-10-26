import sys,collections
from probe import run
from concurrent.futures import ThreadPoolExecutor
ex=ThreadPoolExecutor(2)
pre=(1,39); K=8
X=range(int(sys.argv[1]),int(sys.argv[2]))
def suborbit(y,t):
    P,n,tt=pre,y,t; seq=[]
    for k in range(K):
        r=run(P,n,tt)
        if len(r)<3: break
        P,n,tt,_=r; seq.append((P,n,tt))
    return seq
subs={}
def sj(a): y,t=a; return (y,t),suborbit(y,t)
for key,seq in ex.map(sj,[(y,t) for y in range(X.start-30,X.stop+10) for t in (0,1)]): subs[key]=seq
def job(x):
    n0=6*x; n0+=(-n0)%6
    return x,run(pre+(x,),n0,0)
cnt=collections.Counter(); bad=[]
for x,res in ex.map(job,X):
    P2=res[0]; found=[]
    for (y,t),seq in subs.items():
        for k,(P,n,tt) in enumerate(seq):
            if P+(n,)==P2 or (tt and P+(n,1)==P2): found.append((k+1,x-y,t,tt))
    best=min(found) if found else None
    cnt[(x%6, best[0] if best else None)]+=1
    print(x, x%6, "nested ->",P2, " match (subBells, x-y, t_in, t_out):", sorted(found)[:3])
print(cnt)
