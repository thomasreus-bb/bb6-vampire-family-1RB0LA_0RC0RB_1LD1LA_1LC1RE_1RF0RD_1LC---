import math,sys,time
from map13 import step
n=1; K=int(sys.argv[1]); t0=time.time(); minm=None
for i in range(1,K+1):
    n=step(n)
    if n is None: print('HALT at step',i); break
    if i in (10**3,10**4,10**5,10**6,2*10**6,K): print('step %d: n has %d decimal digits (log10 n = %.1f), %.0fs'%(i,len(str(n)) if i<=2*10**4 else int(n.bit_length()*0.30103)+1,n.bit_length()*0.30103,time.time()-t0),flush=True)
print('done',K)
