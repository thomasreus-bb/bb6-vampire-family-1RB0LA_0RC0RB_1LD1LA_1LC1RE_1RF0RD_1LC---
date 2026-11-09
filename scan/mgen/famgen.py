# generic direct halting test: take real phase descriptions (phc/ph88 output), change every repeat count >= KMIN by a random
# delta in [DLO,DHI] (times DSTEP), expand to cells and run directly (bsim) for STEPS steps
# usage: famgen.py TM file maxlen seed trials steps KMIN DLO DHI DSTEP
import random,subprocess,sys,collections,re
TM,fn,maxlen,seed,T,STEPS,KMIN,DLO,DHI,DSTEP=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),sys.argv[6],int(sys.argv[7]),int(sys.argv[8]),int(sys.argv[9]),int(sys.argv[10])
def expand(d,rnd):
    out=[]
    for t in d.replace('|',' ').split():
        m=re.fullmatch(r'[\(\[]?([01]+)[\)\]]?\^(\d+)',t)
        if m:
            u,k=m.group(1),int(m.group(2))
            if k>=KMIN: k=max(1,k+DSTEP*rnd.randrange(DLO,DHI+1))
            out.append(u*k)
        elif re.fullmatch(r'[01]+',t): out.append(t)
        else: raise ValueError(t)
    return ''.join(out)
L=[]
for l in open(fn):
    if not l.startswith('PH'): continue
    q=[x for x in l.split('|')[0].split() if re.fullmatch('[A-F]',x)][0]
    d=l.split('|',1)[1]
    nums=[int(x) for x in re.findall(r'\^(\d+)',d)]
    if nums and max(nums)*4<maxlen: L.append((q,d))
rnd=random.Random(seed); c=collections.Counter(); ex=[]
for t in range(T):
    q,d=rnd.choice(L); tape=expand(d,rnd).rstrip('0')
    r=subprocess.run(['./bsim',TM,q,tape,STEPS,'Z'],capture_output=True,text=True).stdout.split()
    key=r[0]
    if key=='HALT' and int(r[1])<100: key='HALT_trivial'
    c[key]+=1
    if key=='HALT' and len(ex)<6: ex.append((q,d[:200],r))
print(len(L),'templates',dict(c))
for e in ex: print(e)
