# compare the macro simulator with the accelerated simulator mgen/msim.py (independent method) far beyond direct simulation
import sys,os,re,signal
sys.path.insert(0,'../mgen'); os.environ['TM']='1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE'; os.environ['BS48']='1'
sys.set_int_max_str_digits(0)
from msim import Sim
from ph_desc import describe
from stack70 import blocks
from macro70 import step
NL=int(sys.argv[1])
x,S,steps=30,[11,18,4],1607; want={}
for k in range(NL):
    x,S,d=step(x,S); steps+=d; want[steps]=[1,x]+S
last=max(want); found=[0]; bad=[0]
class Done(Exception): pass
def cb(s):
    if s.steps in want:
        b=blocks(describe([],0,s.R)); nums=[k for v,k in b]
        if s.q==0 and nums==want[s.steps]: found[0]+=1
        else: bad[0]+=1
    if s.steps>last: raise Done()
sm=Sim()
try: sm.run(10**10**5,cb)
except Done: pass
print('macro levels',NL,'(last at 10^%d steps);'%(len(str(last))-1),'msim agrees at',found[0],'level starts, disagrees at',bad[0])
