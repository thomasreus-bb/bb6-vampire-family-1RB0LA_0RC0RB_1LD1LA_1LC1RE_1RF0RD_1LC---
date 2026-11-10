# no. 53 (mirrored): start E-event "11011 0 (1011)^a 1" with random a in [lo,hi), run K E-events (accelerated), report HALT
import os,sys,random,math,signal,time
os.environ['TM']=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1RE_1LC1RE_---1LD_1LE0LB_0RF0LD_1RD1RA'); os.environ.setdefault('BS48','40')
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import hitgen_make
class TO(Exception): pass
class Done(Exception): pass
def _h(a,b): raise TO()
signal.signal(signal.SIGALRM,_h)
seed,T,lo,hi,K,TL=map(int,sys.argv[1:7]); rnd=random.Random(seed)
for t in range(T):
    a=rnd.randrange(lo,hi)
    s=hitgen_make.make2([(1,2),(0,1),(1,2),(0,1),('U','1011',a),(1,1)],4)
    n=[0]
    def cb(s):
        if s.q==4 and s.steps>0:
            n[0]+=1
            if n[0]>=K: raise Done()
    signal.alarm(TL); t0=time.time()
    try: r=s.run(10**400,cb)
    except Done: r='K'
    except TO: r='TIME'
    signal.alarm(0)
    print('T',a,r,n[0],'%.1f'%math.log10(max(s.steps,1)),flush=True)
