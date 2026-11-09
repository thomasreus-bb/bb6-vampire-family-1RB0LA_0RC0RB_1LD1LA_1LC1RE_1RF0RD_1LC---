# phase starts from the accelerated simulator: every left record in state PSTATE (env), tape from the head described
# as compressed cells and (unit)^count for long block runs. MIRROR=1 mirrors the machine (records on the right).
import sys,os,math
M=os.environ['TM']
if os.environ.get('MIRROR')=='1':
    M=M.translate(str.maketrans('LR','RL')); os.environ['TM']=M
import msim
from msim import Sim,BS
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'comp.py')).read().split('for l in sys.stdin')[0])
PS=ord(os.environ.get('PSTATE','C'))-65
MAXC=int(os.environ.get('MAXC','600'))
def per(b):
    s=''.join(map(str,b))
    for L in range(1,len(s)+1):
        if len(s)%L==0 and s==s[:L]*(len(s)//L): return s[:L]
def describe(t,p,R):
    toks=[]; cur=''.join(map(str,t[p:]))
    for b,n in reversed(R):
        if n>3:
            if cur: toks.append(comp(cur)); cur=''
            u=per(b); toks.append('[%s]^%d'%(u,n*BS//len(u)))
        else: cur+=''.join(map(str,b))*n
    if cur: toks.append(comp(cur.rstrip('0')) if cur.rstrip('0') else '')
    s=' '.join(x for x in toks if x)
    return s
def hook(sim,t,p,q,steps):
    if q!=PS: return
    d=describe(t,p,sim.R)
    print('PH %d %.4f | %s'%(steps,math.log10(steps),d[:MAXC]),flush=True)
s=Sim(); s.edgehook=hook
print(s.run(10**int(os.environ.get('CAPEXP','60'))), s.steps)
