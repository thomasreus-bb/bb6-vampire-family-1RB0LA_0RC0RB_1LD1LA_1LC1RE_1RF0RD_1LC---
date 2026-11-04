#!/usr/bin/env python3
"""No. 51: shortest path from r = '' to HALT in the r-graph (graph51.pkl), the residue class of m
that follows it, and an exact check of the path with the macro laws."""
import pickle, sys
from collections import deque
sys.set_int_max_str_digits(0)
G=pickle.load(open('graph51.pkl','rb'))
prev={'':None}; dq=deque(['']); end=None
while dq:
    r=dq.popleft()
    for mod,c,l in G.get(r,[]):
        if l[0]=='HALT': end=(r,mod,c); break
        if l[0]=='C' and l[1] not in prev: prev[l[1]]=(r,mod,c,l); dq.append(l[1])
    if end: break
path=[]; r=end[0]
while prev[r] is not None:
    p,mod,c,l=prev[r]; path.append((p,mod,c,l)); r=p
path.reverse()
L=len(path)+1
print('shortest path to HALT:',L,'macro steps (the last one halts); halting word r =',end[0],'with m =',end[2],'mod',end[1])
def fwd(m):
    """apply the path laws to m; return the list of m_i"""
    ms=[m]
    for p,mod,c,l in path:
        d,mo=l[2]; m0,y0=l[3]; m=y0+(m-m0)*d//mo; ms.append(m)
    return ms
# lift the residue class of the start m step by step
cons=[(mod,c) for p,mod,c,l in path]+[(end[1],end[2])]
a,Mod=0,1
for j,(mod,c) in enumerate(cons):
    # need m_j = c (mod mod); search a + t*Mod
    for t in range(3**6):
        cand=a+t*Mod
        if cand<1: continue
        ms=fwd(cand)
        if all(ms[i]%cons[i][0]==cons[i][1] for i in range(j+1)):
            # also check that m_i are integers (exact): recompute with fractions not needed, laws are exact on classes
            a=cand; break
    Mod*=mod
    a%=Mod
print('start classes: m = %d (mod 3^%d)'%(a, len(str(Mod))*0 + (Mod.bit_length() and round(__import__('math').log(Mod,3)))))
ms=fwd(a if a>40 else a+Mod)
print('smallest such m (> 40) has',len(str(ms[0])),'digits; m before the halting step has',len(str(ms[-1])),'digits')
ok=all(ms[i]%cons[i][0]==cons[i][1] for i in range(len(cons)))
print('residue check along the path:',ok)
open('halt51_path.txt','w').write('\n'.join('%3d  m=%d mod %d  r=%s'%(i+1,c,mod,p) for i,(p,mod,c,l) in enumerate(path))+'\n%3d  m=%d mod %d  r=%s  -> HALT\n'%(L,end[2],end[1],end[0]))
print('start class:',a,'mod',Mod)
