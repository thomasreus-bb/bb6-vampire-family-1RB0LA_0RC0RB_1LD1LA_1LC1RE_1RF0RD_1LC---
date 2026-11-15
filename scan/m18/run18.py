from rules18 import step
import math,collections
n,t=103268,'R4'; maxk=0; cnt=collections.Counter(); E=0
for i in range(100000):
    m,t2=step(n,t)
    if m=='HALT': print('HALT at event',i); break
    k=int(t2[1:]) if len(t2)>1 else 0; maxk=max(maxk,k); cnt[t2[0]]+=1
    n,t=m,t2; E+=1
print('events',E,'digits of n',int(n.bit_length()*0.30103),'max tail index',maxk,'tail types',dict(cnt))
