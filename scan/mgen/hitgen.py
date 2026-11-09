# generic halting experiment: start the accelerated simulator from real left-end events (phc.py output) whose long runs
# are perturbed, run K further left-end events in the states EVS, report HALT / K / TIME
# usage: TM=.. BS48=.. python3 hitgen.py file seed trials K dstep dmax minlen EVS
import os,sys,random,signal,time,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from build import make
from rl import toks_to_rl
fn,seed,T,K,dstep,dmax,minlen,EVS=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]),sys.argv[8]
class Done(Exception): pass
class TO(Exception): pass
def _h(a,b): raise TO()
signal.signal(signal.SIGALRM,_h)
L=[l for l in open(fn) if l.startswith('PH') and l.split()[3] in EVS]
def parse(l):
    d=l.split('|',1)[1]
    # expand periodic long runs into (unit, count) markers handled by a custom run list
    toks=[]
    for t in d.split():
        m=re.fullmatch(r'\[([01]+)\]\^(\d+)',t)
        if m and len(m.group(1))>1: toks.append(('P',m.group(1),int(m.group(2))))
        else: toks.append(('T',t))
    return toks
def expand(toks,rnd):
    rl=[]
    def add(b,n):
        if n<=0: return
        if rl and rl[-1][0]==b: rl[-1]=(b,rl[-1][1]+n)
        else: rl.append((b,n))
    for t in toks:
        if t[0]=='P':
            u,k=t[1],t[2]
            if k>=minlen: k+=dstep*rnd.randrange(dmax//dstep+1) if dmax>0 else 0
            # periodic run of a 2-cell unit: emitted as an explicit long periodic segment (msim blocks of BS cells)
            rl.append(('U',u,k))
        else:
            for b,n in toks_to_rl(t[1]): add(b,n)
    return rl
def to_blocks_rl(rl):
    # flatten into a cell-run list, periodic units stay compressed via a generator in build
    out=[]
    for x in rl:
        if x[0]=='U': out.append(x)
        else: out.append(x)
    return out
import build
from msim import BS
def make2(rl,q):
    # like build.make but supports periodic units
    blocks=[]; buf=[]
    def emit(blk,n):
        if blocks and blocks[-1][0]==blk: blocks[-1][1]+=n
        else: blocks.append([blk,n])
    def push_cells(cells):
        nonlocal buf
        for c in cells:
            buf.append(c)
            if len(buf)==BS: emit(tuple(buf),1); buf=[]
    for x in rl:
        if x[0]=='U':
            u=[int(c) for c in x[1]]; k=x[2]; n=k*len(u)
            # fill buffer with whole cells until aligned, then bulk blocks, then remainder
            i=0
            while buf and n>0: push_cells([u[i%len(u)]]); i+=1; n-=1
            if n>=BS:
                blk=tuple(u[(i+j)%len(u)] for j in range(BS)); m=n//BS; emit(blk,m)
                i+=m*BS; n-=m*BS
            while n>0: push_cells([u[i%len(u)]]); i+=1; n-=1
        else:
            b,n=x
            while buf and n>0: push_cells([b]); n-=1
            if n>=BS: emit((b,)*BS,n//BS); n%=BS
            push_cells([b]*n)
    if buf: emit(tuple(buf+[0]*(BS-len(buf))),1)
    s=build.Sim(); s.R=[list(x) for x in reversed(blocks)]; s.L=[]; s.q=q; s.d='L'; s.steps=0
    return s
rnd=random.Random(seed)
for t in range(T):
    i=rnd.randrange(len(L)//3,len(L)-1)
    l=L[i]; q=ord(l.split()[3])-65
    rl=expand(parse(l),rnd)
    s=make2(rl,q); n=[0]
    def cb(s):
        if chr(65+s.q) in EVS and s.steps>0:
            n[0]+=1
            if n[0]>=K: raise Done()
    signal.alarm(int(os.environ.get('TLIM','30'))); t0=time.time()
    try: r=s.run(10**int(os.environ.get('CAPEXP','400')),cb)
    except Done: r='K'
    except TO: r='TIME'
    signal.alarm(0)
    print('T',i,r,n[0],s.halt,'%.0fs'%(time.time()-t0),flush=True)
