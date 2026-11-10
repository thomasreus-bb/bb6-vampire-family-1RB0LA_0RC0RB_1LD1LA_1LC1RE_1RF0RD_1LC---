# no. 53 (mirrored): start "11011 0 (1011)^a 1" (state E, head at the end) with random a in [lo,hi); run to 10^(2 log10(4a) + X) steps
import os,sys,random,math,signal,time
os.environ['TM']=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1RE_1LC1RE_---1LD_1LE0LB_0RF0LD_1RD1RA'); os.environ.setdefault('BS48','40')
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import hitgen_make
class TO(Exception): pass
def _h(a,b): raise TO()
signal.signal(signal.SIGALRM,_h)
seed,T,lo,hi,X,TL=map(int,sys.argv[1:7]); rnd=random.Random(seed)
for t in range(T):
    a=rnd.randrange(lo,hi)
    s=hitgen_make.make2([(1,2),(0,1),(1,2),(0,1),('U','1011',a),(1,1)],4)
    cap=10**int(2*math.log10(4*a)+X)
    signal.alarm(TL); t0=time.time()
    try: r=s.run(cap)
    except TO: r='TIME'
    signal.alarm(0)
    print('T',a,r,'%.1f'%math.log10(max(s.steps,1)),'%.1f'%math.log10(cap),'%.0fs'%(time.time()-t0),flush=True)
