import sys
from probe import run
P=tuple(map(int,sys.argv[1].split(","))) if sys.argv[1]!="-" else ()
n=int(sys.argv[2]); t=int(sys.argv[3]); k=int(sys.argv[4])
for i in range(k):
    r=run(P,n,t)
    if len(r)<3: print(r); break
    P,n,t,st=r; print(i+1,P,n,t,st)
