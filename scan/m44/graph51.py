#!/usr/bin/env python3
"""No. 51: build the graph of memory words r (BFS from r = ''), with the exact macro law per residue class,
save it (graph51.pkl), and report the shortest path to HALT and the distances to HALT."""
import os, sys, time, pickle
from collections import deque
from rmodel51 import rules
N=int(sys.argv[1]) if len(sys.argv)>1 else 300000
G={}; dq=deque(['']); seen={''}; t0=time.time()
while dq and len(G)<N:
    r=dq.popleft(); rs=rules(r); G[r]=rs
    for mod,c,l in rs:
        if l[0]=='C' and l[1] not in seen: seen.add(l[1]); dq.append(l[1])
    if len(G)%20000==0: print(len(G),'words %.0fs'%(time.time()-t0), flush=True)
pickle.dump(G,open(os.environ.get('TMTAG','51').join(['graph','.pkl']),'wb'))
# reverse BFS: distance (number of macro steps) to HALT
rev={}
halt=[]
for r,rs in G.items():
    for mod,c,l in rs:
        if l[0]=='HALT': halt.append(r)
        elif l[0]=='C': rev.setdefault(l[1],[]).append(r)
dist={r:1 for r in halt}; dq=deque(halt)
while dq:
    r=dq.popleft()
    for p in rev.get(r,[]):
        if p not in dist: dist[p]=dist[r]+1; dq.append(p)
pickle.dump(dist,open(os.environ.get('TMTAG','51').join(['dist','.pkl']),'wb'))
print('words',len(G),'halting words',len(set(halt)),'words with a path to HALT',len(dist),'distance of r="":',dist.get(''))
