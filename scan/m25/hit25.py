# no. 25: from the outer phase start 1 0 1^N T (state D, head at the left end) with random N, run to the next outer phase or HALT
import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import os,sys,random,math,signal,time
os.environ['TM']='1RB0LE_1LC0RD_0RA1LD_0LC1RA_1LF1LA_---1LA'; os.environ.setdefault('BS48','12')
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from build import make
from ph_desc import describe
from rl import toks_to_rl
class Done(Exception): pass
class TO(Exception): pass
def _h(a,b): raise TO()
signal.signal(signal.SIGALRM,_h)
TAILS={'e':[],'2':[(0,1),(1,2)],'7':[(0,1),(1,7),(0,1),(1,2)],'17':[(0,1),(1,17),(0,1),(1,2)],'54':[(0,1),(1,54)]}
def run1(N,T,cap=10**400):
    tl=[] if T=='e' else sum([[(0,1),(1,int(x))] for x in T.split('.')],[])
    rl=[(1,1),(0,1),(1,N)]+tl
    s=make(rl,3); res={}
    def cb(s):
        if s.q==3 and s.steps>0:
            res['d']=describe([],0,s.R); raise Done()
    try: r=s.run(cap,cb)
    except Done: r='D'
    return r,s,res.get('d')
if __name__=='__main__':
    seed=int(sys.argv[1]); T=int(sys.argv[2]); lo,hi=int(sys.argv[3]),int(sys.argv[4]); tails=sys.argv[5].split(',')
    rnd=random.Random(seed)
    for t in range(T):
        tl=rnd.choice(tails); N=rnd.randrange(lo,hi)
        signal.alarm(30)
        try: r,s,d=run1(N,tl)
        except TO: print('T',tl,N,'TIME',flush=True); continue
        signal.alarm(0)
        if r=='HALT': print('T',tl,N,'HALT',s.halt,flush=True)
        else:
            rl=toks_to_rl(d); N2=rl[2][1] if len(rl)>2 else 0
            tail=''.join(('%d'%n)+('' if b else "'") for b,n in rl[3:])
            print('T',tl,N,r,'%.3f'%(math.log(max(N2,1)/N)/math.log(4/3)),tail,flush=True)
