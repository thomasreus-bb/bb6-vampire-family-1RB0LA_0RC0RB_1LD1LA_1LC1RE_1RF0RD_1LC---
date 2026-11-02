# fast run of no. 41: report every left-end event in states A and B
import sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','m95'))
import fast
class AnyState:
    def __eq__(self,o): return o in (0,1)
fast.REPORT_STATE=AnyState()
M='1RB1LD_1RC0RA_1LA1RE_0LA0LB_0RB1RF_---1RD'
LIM=10**int(sys.argv[1])
class Stop(Exception): pass
def rep(S,out):
    if S.steps>LIM: raise Stop
    print('AB'[S.s], S.steps, ' '.join('(%s)^%d'%(w,c) if c>1 else w for w,c in out)[:300], flush=True)
try: S=fast.run2(M,10**400,9,rep)
except Stop: pass
