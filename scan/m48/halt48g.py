# halting B for prefix 010101, empty near tail, one gap of G zeros followed by the marker X
import sys
from pmap48 import *
X='1'+'100'*3+'0110011001'
G=int(sys.argv[1]); lo,hi,stepB=int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
h=[];n=0
for B in range(lo,hi,stepB):
    r=step(build('010101',B,'',[(G,X)] if G>0 else []),200.0*B*B+1e6); n+=1
    if r[0]=='HALT': h.append(B)
print('gap',G,'B in [%d,%d) step %d: %d tested, %d HALT:'%(lo,hi,stepB,n,len(h)),h,'residues mod 70:',sorted(set(b%70 for b in h)),flush=True)
