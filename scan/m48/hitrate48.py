# fraction of random (B, G) with prefix 010101, empty near tail, B = 0 mod 5 and one gap G < B that halt within one phase
import sys,random
from pmap48 import *
X='1'+'100'*3+'0110011001'
lo,hi,n,seed=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
random.seed(seed); h=[]
for i in range(n):
    B=5*random.randrange(lo//5,hi//5); G=random.randrange(int(0.05*B),int(0.9*B))
    r=step(build('010101',B,'',[(G,X)]),300.0*B*B+1e6)
    if r[0]=='HALT': h.append((B,G))
print('B in [%d,%d): %d samples, %d HALT'%(lo,hi,n,len(h)),h,flush=True)
