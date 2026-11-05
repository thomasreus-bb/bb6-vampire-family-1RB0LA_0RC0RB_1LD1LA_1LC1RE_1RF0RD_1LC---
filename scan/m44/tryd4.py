import sys, time
from prestar import prestar, accepts
import dfas
TM=sys.argv[1]; R,CAP,MOD,AMOD=map(int,sys.argv[2:6])
NQ,delta,lst=dfas.make3(R,CAP,MOD,AMOD)
t=time.time(); trans,ctl,F=prestar(TM,NQ,delta)
print('R=%d CAP=%d MOD=%d AMOD=%d NQ=%d  start could halt:'%(R,CAP,MOD,AMOD,NQ), accepts(trans,ctl(0,0,0),[2],F), '%.0fs'%(time.time()-t), flush=True)
