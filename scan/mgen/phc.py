# like ph.py but without cell-level edge: describe the tape whenever the head is at the left end of the stored tape
# (macro granularity). FILTER: python expression on d (description string) and s (sim)
import sys,os,math
M=os.environ['TM']
if os.environ.get('MIRROR')=='1':
    M=M.translate(str.maketrans('LR','RL')); os.environ['TM']=M
from msim import Sim,BS
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'comp.py')).read().split('for l in sys.stdin')[0])
from ph_desc import describe
MAXC=int(os.environ.get('MAXC','600')); FIL=os.environ.get('FILTER','True')
last=[None]
def cb(s):
    d=describe([],0,s.R)
    if eval(FIL):
        print('PH %d %.4f %s | %s'%(s.steps,math.log10(max(s.steps,1)),chr(65+s.q),d[:MAXC]),flush=True)
s=Sim()
print(s.run(10**int(os.environ.get('CAPEXP','60')),cb), s.steps, s.halt)
