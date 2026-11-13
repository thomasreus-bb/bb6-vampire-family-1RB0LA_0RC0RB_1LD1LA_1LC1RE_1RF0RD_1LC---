#!/usr/bin/env python3
"""Real trajectory at the macro level C(m, r) of the table of no. 51, from C(M0, R0) (environment variables).
m' = y0 + (m - m0) * d / mod for the residue class (mod, c) of m (law sampled by rmodel51.rules)."""
import os, sys, pickle, os
from rmodel51 import rules
sys.set_int_max_str_digits(0)
dist=pickle.load(open(os.environ.get('TMTAG','51').join(['dist','.pkl']),'rb')) if os.path.exists(os.environ.get('TMTAG','51').join(['dist','.pkl'])) else {}
cache={}
def macro(m,r):
    if r not in cache: cache[r]=rules(r)
    for mod,c,l in cache[r]:
        if m%mod==c:
            if l[0]=='HALT': return 'HALT',None
            if l[0]=='?': return '?',None
            d,mo=l[2]; m0,y0=l[3]
            return l[1], y0+(m-m0)*d//mo
    return '?',None
m,r=int(os.environ.get('M0','10')),os.environ.get('R0',''); K=int(sys.argv[1]) if len(sys.argv)>1 else 300
best=None
for k in range(K):
    dd=dist.get(r)
    if dd is not None and (best is None or dd<best[0]): best=(dd,k,r)
    if k<40 or k%25==0: print(k, 'm has %d digits'%len(str(m)), 'm mod 3 =',m%3, 'r =',r if len(r)<60 else r[:60]+'...', 'dist to HALT:',dd)
    r2,m2=macro(m,r)
    if r2 in ('HALT','?'): print('stop',r2,k); break
    r,m=r2,m2
print('closest approach (macro steps to HALT, at step, r):',best)
