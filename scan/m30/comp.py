import sys,re
# compress a 0/1 string: runs of a repeated unit (len 1..4) of >=3 repetitions -> (u)^k
def comp(s):
    out=[];i=0;n=len(s)
    while i<n:
        best=None
        for L in (1,2,3,4):
            u=s[i:i+L]
            if len(u)<L: break
            k=1
            while s[i+k*L:i+(k+1)*L]==u: k+=1
            if k>=3 and (best is None or k*L>best[1]*len(best[0])): best=(u,k)
        if best: out.append(f"({best[0]})^{best[1]}" if len(best[0])>1 else f"{best[0]}^{best[1]}"); i+=len(best[0])*best[1]
        else: out.append(s[i]); i+=1
    return ' '.join(out)
for l in sys.stdin:
    f=l.split()
    if len(f)<3: print(l.strip()); continue
    print(f[0], comp(f[2]))
