import sys
from prestar import prestar, accepts
import dfas
TM=sys.argv[1]; K,M1,M2=map(int,sys.argv[2:5])
NQ,delta,lst=dfas.make(K,M1,M2)
trans,ctl,F=prestar(TM,NQ,delta)
print('K=%d M1=%d M2=%d NQ=%d  start could halt:'%(K,M1,M2,NQ), accepts(trans,ctl(0,0,0),[2],F), flush=True)
