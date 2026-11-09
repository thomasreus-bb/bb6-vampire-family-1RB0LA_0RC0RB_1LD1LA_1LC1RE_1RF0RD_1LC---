# run the accelerated simulator on one machine for a fixed wall time; print reached steps, halt, tape size
import sys,time,os,math,signal
from msim import Sim
T=int(sys.argv[1])
class Stop(Exception): pass
def h(sig,frm): raise Stop()
signal.signal(signal.SIGALRM,h); signal.alarm(T)
s=Sim(); res='TIME'
try:
    r=s.run(10**int(os.environ.get("CAPEXP","300")))
    res=r
except Stop: pass
except Exception as e:
    res='ERR:'+str(e)[:40]
signal.alarm(0)
cells=sum(n for b,n in s.L+s.R)*int(os.environ.get('BS48','40'))
st=s.halt if res=='HALT' else s.steps
print(os.environ['TM'], res, 'steps=%.3e'%st, 'log10=%.1f'%(math.log10(max(st,1))), 'runs=%d'%(len(s.L)+len(s.R)), 'cells=%.2e'%cells, 'jumps=%d'%s.jumps, flush=True)
