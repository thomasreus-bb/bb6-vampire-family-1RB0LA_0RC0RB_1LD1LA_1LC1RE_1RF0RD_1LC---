# halting rate of no. 88 from perturbed real phase starts: every zero gap longer than 1000 cells gets a random even extra 0..38 cells (odd changes break the parity of the gaps)
import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import sys,random,time
import exp88,signal
class TO(Exception): pass
def _h(a,b): raise TO()
signal.signal(signal.SIGALRM,_h)
P=exp88.load()
seed=int(sys.argv[1]); T=int(sys.argv[2]); K=int(sys.argv[3])
rnd=random.Random(seed)
for t in range(T):
    while True:
        i=rnd.randrange(30,int(__import__("os").environ.get("IMAX","250")))
        try: q,rl=exp88.parse(P[i]); break
        except Exception: pass
    rl2=[(b,n+(2*rnd.randrange(20) if b==0 and n>1000 else 0)) for b,n in rl]
    t0=time.time()
    signal.alarm(20)
    try: r,s,out=exp88.phases(rl2,q,K)
    except TO:
        print('T',i,'TIME',flush=True); continue
    signal.alarm(0)
    print('T',i,r,len(out),s.halt is not None,s.steps,'%.0fs'%(time.time()-t0),flush=True)
