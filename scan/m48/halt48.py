# halting fraction of one phase of no. 48 for built phase-start tapes  prefix (1001)^B near  (no gaps)
import sys,random
from pmap48 import *
pre=sys.argv[1]; near=sys.argv[2] if sys.argv[2]!='-' else ''
lo,hi,n=int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5])
random.seed(lo)
Bs=list(range(lo,hi)) if hi-lo<=n else sorted(random.sample(range(lo,hi),n))
h=[];m=0
for B in Bs:
    r=step(build(pre,B,near,[]),200.0*B*B+1e6)
    if r[0]=='HALT': h.append(B)
    elif r[0]=='MAX': m+=1
print(pre,near or '-','B in [%d,%d): %d tested, %d HALT, %d MAX; halting B: %s'%(lo,hi,len(Bs),len(h),m,h[:30]),flush=True)
