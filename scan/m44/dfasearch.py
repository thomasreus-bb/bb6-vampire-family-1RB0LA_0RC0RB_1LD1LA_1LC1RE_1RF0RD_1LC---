#!/usr/bin/env python3
"""Search all DFAs with n states (canonical BFS numbering, delta(0,0) = 0) for one that makes the
pre* test succeed (start configuration not in pre*(HALT)).  usage: dfasearch.py TM n"""
import sys, time
from prestar import prestar, accepts
TM=sys.argv[1]; n=int(sys.argv[2])
def gen(n):
    # table as list of 2n entries: entry 2q+c = delta(q,c); canonical: states first appear in order 1,2,...
    tab=[None]*(2*n); tab[0]=0
    def rec(i, maxs):
        if i==2*n:
            if maxs==n-1: yield list(tab)
            return
        q=i//2
        if q>maxs: return            # state q not yet reachable -> not canonical
        for v in range(0, min(maxs+2, n)):
            tab[i]=v
            yield from rec(i+1, max(maxs,v))
    yield from rec(1,0)
t0=time.time(); cnt=0
for tab in gen(n):
    cnt+=1
    trans,ctl,F=prestar(TM,n,lambda q,c: tab[2*q+c])
    if not accepts(trans,ctl(0,0,0),[2],F):
        print('FOUND', n, tab, flush=True); break
    if cnt%20000==0: print(cnt,'DFAs tested, %.0fs'%(time.time()-t0), flush=True)
print('done',cnt,'DFAs, %.0fs'%(time.time()-t0))
