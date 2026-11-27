import subprocess,random,re,sys,json
from collections import Counter
TM=sys.argv[1]; raw=sys.argv[2]; idxs=[int(x) for x in sys.argv[3].split(',')]; T=int(sys.argv[4]); seed=int(sys.argv[5]); LMAX=int(sys.argv[6])
L=[l.split() for l in open(raw)]
rnd=random.Random(seed)
def toks(t):
    lead=len(t)-len(t.lstrip('0')); return lead,[m.group(0) for m in re.finditer(r'(1+)(0*)',t[lead:])]
def perturb(t):
    lead,tk=toks(t)
    for j in range(rnd.randint(1,3)):
        i=rnd.randrange(40,max(41,len(tk)-20))
        if tk[i]=='100': tk[i]='1000'
        elif tk[i]=='1000' and rnd.random()<0.5: tk[i]='100'
    return '0'*lead+''.join(tk)
sig=Counter(); res=Counter(); halts=[]
for it in range(T):
    t=L[rnd.choice(idxs)][2]
    while len(t)<LMAX:
        t=perturb(t)
        o=subprocess.run(['/tmp/an78/pass78',TM,'E','20000000000'],input=t+'\n',capture_output=True,text=True).stdout.splitlines()
        Ts=[int(x.split()[1]) for x in o if x.startswith('T ')]
        end=[x for x in o if x.startswith('END')][0].split()
        # split into passes
        passes=[];cur=[]
        for v in Ts:
            if cur and v>cur[-1]: passes.append(cur);cur=[]
            cur.append(v)
        if cur: passes.append(cur)
        for k,pz in enumerate(passes):
            low=tuple(x for x in pz if x<130)
            kind='REC' if k==len(passes)-1 and end[1]=='REC' else ('HALT' if k==len(passes)-1 and end[1]=='HALT' else 'reset')
            sig[(low[:3],kind)]+=1
        res[end[1]]+=1; res['passes%d'%len(passes)]+=1
        if end[1]!='REC': halts.append((end,len(t))); break
        t=o[-1]
print(json.dumps({'res':res,'halts':halts}))
for k,v in sorted(sig.items(),key=lambda kv:-kv[1]): print(v,k)
