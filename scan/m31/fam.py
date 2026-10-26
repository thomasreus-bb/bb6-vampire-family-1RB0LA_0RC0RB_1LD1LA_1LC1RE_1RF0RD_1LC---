import sys
from probe import run
from concurrent.futures import ThreadPoolExecutor
ex=ThreadPoolExecutor(2)
pre=tuple(map(int,sys.argv[1].split(","))) if sys.argv[1]!="-" else ()
post=tuple(map(int,sys.argv[2].split(","))) if sys.argv[2]!="-" else ()
t=int(sys.argv[3]); xs=range(int(sys.argv[4]),int(sys.argv[5])); nf=int(sys.argv[6]) if len(sys.argv)>6 else 10
for x in xs:
    n0=nf*x; n0+= (-n0)%6
    fs=[(r,ex.submit(run,pre+(x,)+post,n0+r,t)) for r in range(6)]
    out=[]
    for r,f in fs:
        res=f.result()
        if len(res)<3: out.append("%d:%s"%(r,res[0])); continue
        P2,n2,t2,st=res
        n=n0+r
        d = "4n/3%+.2f"%(n2-4*n/3) if abs(n2-4*n/3)<abs(n2-n) else "n%+d"%(n2-n)
        out.append("%d:%s|%d %s"%(r,",".join(map(str,P2)),t2,d))
    print("x=%d x%%6=%d"%(x,x%6),"  ".join(out),flush=True)
