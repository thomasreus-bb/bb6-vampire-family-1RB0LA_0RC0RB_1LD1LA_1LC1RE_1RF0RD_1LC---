# no. 53 (mirrored): start from (1011)^a 1 in state A with random a, run the accelerated simulator to 10^CAP steps
import os,sys,random,math,signal,time
os.environ['TM']=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1RE_1LC1RE_---1LD_1LE0LB_0RF0LD_1RD1RA'); os.environ.setdefault('BS48','40')
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import hitgen_make
class TO(Exception): pass
def _h(a,b): raise TO()
signal.signal(signal.SIGALRM,_h)
seed,T,lo,hi,CAP,TL=map(int,sys.argv[1:7]); rnd=random.Random(seed)
for t in range(T):
    a=rnd.randrange(lo,hi)
    s=hitgen_make.make2([('U','1011',a),(1,1)],0)
    signal.alarm(TL); t0=time.time()
    try: r=s.run(10**CAP)
    except TO: r='TIME'
    signal.alarm(0)
    print('T',a,r,'%.2f'%math.log10(max(s.steps,1)),'%.0fs'%(time.time()-t0),flush=True)
