#!/usr/bin/env python3
"""BFS over the memory word r of no. 51: shortest residue path from r = '' to HALT."""
import sys, time
from rmodel51 import rules
from collections import deque
start=sys.argv[1] if len(sys.argv)>1 else ''
limit=int(sys.argv[2]) if len(sys.argv)>2 else 10**6
prev={start:None}; dq=deque([start]); R={}; t0=time.time(); unknown=[]; halts=[]
while dq and len(prev)<limit:
    r=dq.popleft(); rs=rules(r); R[r]=rs
    for mod,c,l in rs:
        if l[0]=='HALT': halts.append((r,mod,c)); continue
        if l[0]=='?': unknown.append((r,mod,c)); continue
        r2=l[1]
        if r2 not in prev: prev[r2]=(r,mod,c); dq.append(r2)
    if halts: break
    if len(prev)%5000==0: print(len(prev),'words', 'queue',len(dq), 'maxlen',max(map(len,prev)), '%.0fs'%(time.time()-t0), flush=True)
print('visited',len(R),'words, seen',len(prev),'unknown',len(unknown),'halts',len(halts))
if halts:
    r,mod,c=halts[0]; path=[(r,mod,c,'HALT')]
    while prev[r] is not None:
        p,mo,cc=prev[r]; path.append((p,mo,cc,r)); r=p
    path.reverse(); print('path length',len(path))
    for p in path: print(p)
print('unknown sample',unknown[:5])
