# long run of the accelerated simulator for no. 48.
# PHASE lines: the left end is reached while the leading run of 0101 blocks is short (< 50 blocks)
#              after it had been long (> 1000 blocks) since the previous PHASE line.
# STATUS lines every 30 s.
import sys,time
from msim48 import Sim
T=float(sys.argv[1])
s=Sim(); t0=time.time(); mx=[0]; lastp=[time.time()]
def rle(s):
    return ' '.join('%s^%d'%(''.join(map(str,b)),n) for b,n in reversed(s.R))
def cb(s):
    first=s.R[-1] if s.R else None
    a=first[1] if first and first[0]==(0,1)*(len(first[0])//2) else 0
    if a>mx[0]: mx[0]=a
    if mx[0]>1000 and a<50:
        print('PHASE step=%d t=%.0fs state=%s | %s'%(s.steps,time.time()-t0,'ABCDEF'[s.q],rle(s)),flush=True)
        mx[0]=0
    if time.time()-lastp[0]>30:
        lastp[0]=time.time()
        print('STATUS step=%.4e t=%.0fs jumps=%d | %s'%(s.steps,time.time()-t0,s.jumps,rle(s)[:300]),flush=True)
r=s.run(T,cb)
print(r,'steps=%d'%(s.halt if r=='HALT' else s.steps),'t=%.0fs'%(time.time()-t0),'jumps',s.jumps,flush=True)
print('TAPE',rle(s))
