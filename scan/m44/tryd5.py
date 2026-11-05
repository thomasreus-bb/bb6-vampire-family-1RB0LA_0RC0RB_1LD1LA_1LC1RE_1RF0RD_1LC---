import sys, time
from prestar import prestar, accepts
import dfas
TM=sys.argv[1]; L,K,CA=map(int,sys.argv[2:5])
NQ,delta,lst=dfas.make4(L,K,CA)
t=time.time(); trans,ctl,F=prestar(TM,NQ,delta)
print('L=%d K=%d CAPA=%d NQ=%d  start could halt:'%(L,K,CA,NQ), accepts(trans,ctl(0,0,0),[2],F), '%.0fs'%(time.time()-t), flush=True)
