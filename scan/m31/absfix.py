# abstract fixpoint at macro-step level: class = (head gap from the right end, tokens); token = exact value below S, else 'B' + residue mod M
import sys,random,subprocess,collections,pickle
S=int(sys.argv[1]); M=int(sys.argv[2]); SAMP=int(sys.argv[3]); ROUNDS=int(sys.argv[4]); seed=int(sys.argv[5])
rnd=random.Random(seed)
def cls(h,bl): return (len(bl)-h,)+tuple(x if x<S else 'B%d'%(x%M) for x in bl)
def member(c):
    r=c[0]; bl=[]
    for t in c[1:]:
        if isinstance(t,int): bl.append(t)
        else:
            res=int(t[1:]); big=rnd.choice([1,2,3,5,10,30,100,400,3000]); kmin=-(-(S-res)//M)
            x=res+M*rnd.randrange(kmin,kmin+big); bl.append(x)
    return len(bl)-r,bl
def stepb(cfgs):
    inp=''.join('%d %s\n'%(h,' '.join(map(str,bl))) for h,bl in cfgs)
    out=subprocess.run(['./mb','1','100000000'],input=inp,capture_output=True,text=True).stdout.split('\n')
    res=[]
    for o in out[:len(cfgs)]:
        f=o.split()
        if f[0]!='OK': res.append((f[0],None)); continue
        res.append((int(f[2]),list(map(int,f[4:]))))
    return res
# seeds: classes of the real orbit
C=set()
for l in open('snaps.txt'):
    a,b=l.split('|'); t=b.split(); h=int(t[-1][1:]); bl=list(map(int,t[:-1]))
    # snaps2 counts h like mstep? check below with the tool itself
    C.add(cls(h+1 if h<len(bl) else h,bl))
print('seed classes from the orbit:',len(C))
frontier=set(C); halts=[]
for rd in range(ROUNDS):
    batch=[];src=[]
    for c in frontier:
        for _ in range(SAMP): batch.append(member(c)); src.append(c)
    new=set(); nh=0
    for (h,bl),c,(h2,bl2) in zip(batch,src,stepb(batch)):
        if bl2 is None:
            if h2=='HALT': halts.append((c,h,bl)); nh+=1
            continue
        d=cls(h2,bl2)
        if d not in C: new.add(d)
    C|=new; frontier=new
    print('round',rd,'classes',len(C),'new',len(new),'halting samples',nh,flush=True)
    if not new or len(C)>60000: break
hc=collections.Counter(c for c,h,bl in halts)
print('halting classes:',len(hc))
for c,v in hc.most_common(8):
    ex=next((h,bl) for cc,h,bl in halts if cc==c); print('  ',v,c,'e.g. h=%d'%ex[0],ex[1])
pickle.dump((C,halts),open('absfix_%d_%d.pkl'%(S,M),'wb'))
