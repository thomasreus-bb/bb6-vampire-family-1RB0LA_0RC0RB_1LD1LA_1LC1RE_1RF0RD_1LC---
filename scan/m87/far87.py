# accelerated run of no. 87 (mgen/msim.py): print the left-edge events (state A) with a short description
import sys,os,signal
sys.path.insert(0,'../mgen'); os.environ['TM']='1RB1LC_1RC0RF_1RD0LB_1RE0LD_1LF---_0RA1LA'
os.environ.setdefault('BS48','6'); sys.set_int_max_str_digits(0)
from msim import Sim
from ph_desc import describe
class Stop(Exception): pass
signal.signal(signal.SIGALRM,lambda a,b:(_ for _ in ()).throw(Stop())); signal.alarm(int(sys.argv[1]))
last=[None]
def cb(s):
    if s.q!=0: return
    d=describe([],0,s.R)
    if len(d)<160:
        print('10^%.3f'%(len(str(s.steps))-1+float('0.'+str(s.steps)[:3])), d, flush=True)
s=Sim()
try: print(s.run(10**10**5,cb))
except Stop: print('time up, steps ~10^%d'%(len(str(s.steps))-1))
