# accelerated run (mgen/msim.py, heuristic loop skipping) for a fixed wall time; prints the number of digits of the step count
# usage: TM=... BS48=12 python3 far70.py seconds
import sys,os,signal
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'../mgen'))
sys.set_int_max_str_digits(0)
from msim import Sim
class Stop(Exception): pass
def h(a,b): raise Stop()
signal.signal(signal.SIGALRM,h); signal.alarm(int(sys.argv[1]))
s=Sim(); res='TIME'
try: res=s.run(10**int(os.environ.get('CAPEXP','10**6'.replace('10**','')) ))
except Stop: pass
signal.alarm(0)
st=s.halt if res=='HALT' else s.steps
print(os.environ['TM'],res,'step count has',len(str(st)),'digits; runs',len(s.L)+len(s.R),'jumps',s.jumps,flush=True)
