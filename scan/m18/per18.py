import sys; sys.path.insert(0,'.')
from rules18 import step
n,t=103268,'R4'; seq=[]; mk=0
for i in range(300000):
    m,t2=step(n,t)
    if m=='HALT': print('HALT at event',i); sys.exit()
    seq.append(t2[0]+('' if t2=='S' else '')); k=int(t2[1:]) if len(t2)>1 else 0; mk=max(mk,k)
    n,t=m,t2
tt=seq[-8000:]
per=[p for p in range(1,3000) if all(tt[i]==tt[i+p] for i in range(len(tt)-p))]
print('events',len(seq),'max k',mk,'digits',int(n.bit_length()*0.30103),'eventual period:',per[:3])
