import subprocess,sys
def run(P,n,t,mx=10**11):
    args=["./one",str(mx)]+[str(x) for x in P]+[str(n)]+(["1"] if t else [])
    o=subprocess.run(args,capture_output=True,text=True).stdout.strip()
    if not o.startswith("OK"): return (o.split()[0],)
    st=int(o.split()[1]); r=o.split("|")[1].split()
    if any(x.startswith("z") for x in r): return ("ODD",tuple(r))
    r=list(map(int,r))
    tail = len(r)>=2 and r[-1]==1 and r[-2]>1
    mi=len(r)-2 if tail else len(r)-1
    return (tuple(r[:mi]), r[mi], int(tail), st)
if __name__=="__main__":
    P=tuple(map(int,sys.argv[1].split(","))) if sys.argv[1]!="-" else ()
    t=int(sys.argv[2]); n0=int(sys.argv[3]); k=int(sys.argv[4])
    for n in range(n0,n0+k):
        r=run(P,n,t)
        if len(r)<3: print(n,r); continue
        P2,n2,t2,st=r
        print(n, n%27, P2, t2, "n'-4n/3=%.3f"%(n2-4*n/3), "n'-n=%d"%(n2-n))
