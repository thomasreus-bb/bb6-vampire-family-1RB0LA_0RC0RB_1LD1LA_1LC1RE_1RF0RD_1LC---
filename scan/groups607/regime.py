# Compare the behaviour of the members of each same-table group (the first member X started in different states).
# Features of a run (X started in state s, blank tape, N steps):
#  - token bag of the tapes at the records in the second half: repeated short words (w)* and the literal pieces between them
#  - growth exponent of the tape width (log width / log steps between N/4 and N)
#  - share of records on the left side
# Two runs count as "same regime" when the cosine similarity of the token bags is >= 0.8 and the growth exponents
# differ by less than 0.1.  usage: python3 regime.py N -> regime.json
import json,itertools,subprocess,sys,math,collections
from fingerprint import shape
g=json.load(open('groups607.json')); info={int(k):v for k,v in json.load(open('info607.json')).items()}
S='ABCDEF'
def parse(t):
    d={}
    for i,gg in enumerate(t.split('_')):
        for b in (0,1):
            x=gg[3*b:3*b+3]; d[(S[i],b)]=None if x[0]=='-' else (x[0],x[1],x[2])
    return d
def start_in_X(Y,X):
    dy=parse(Y); dx=parse(X)
    for mir in (0,1):
        for p in itertools.permutations(S):
            P=dict(zip(S,p))
            t={(P[q],b):(None if v is None else (v[0],({'L':'R','R':'L'}[v[1]] if mir else v[1]),P[v[2]])) for (q,b),v in dx.items()}
            if t==dy: return [k for k,v in P.items() if v=='A'][0]
def tokens(sh):
    import re
    parts=re.split(r'(\([01]+\)\*)',sh)
    out=[]
    for p in parts:
        if not p: continue
        if p.endswith('*'): out.append(p)
        else:
            for i in range(0,len(p),8): out.append(p[i:i+8])
    return out
def features(X,s,N):
    r=subprocess.run(['./recs',X,s,str(N),'25','30000'],capture_output=True,text=True).stdout.split('\n')
    recs=[l.split() for l in r if l and l[0].isdigit()]
    if any(l.startswith('HALT') for l in r): return {'halt':True}
    steps=[int(x[0]) for x in recs]; sides=[x[1] for x in recs]
    width=len(recs)  # one record per new cell (+1)
    tapes=[x[3] for x in recs[len(recs)//2:] if len(x)>3 and x[3]!='-']
    bag=collections.Counter()
    step=max(1,len(tapes)//400)
    for t in tapes[::step]: bag.update(set(tokens(shape(t))))
    # growth exponent between N/4 and N
    def w_at(n):
        k=sum(1 for x in steps if x<=n); return max(k,1)
    # growth exponent: least-squares slope of log(width) against log(steps) over the records after step N/1000
    pts=[(math.log(st+1),math.log(i+1)) for i,st in enumerate(steps) if st>=N/1000]
    if len(pts)>5:
        mx=sum(p[0] for p in pts)/len(pts); my=sum(p[1] for p in pts)/len(pts)
        e=sum((p[0]-mx)*(p[1]-my) for p in pts)/max(1e-12,sum((p[0]-mx)**2 for p in pts))
    else: e=0.0
    return {'halt':False,'bag':dict(bag),'exp':e,'left':sides.count('L')/max(1,len(sides)),'width':w_at(N)}
def cos(a,b):
    keys=set(a)|set(b); dot=sum(a.get(k,0)*b.get(k,0) for k in keys)
    na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values()))
    return dot/(na*nb) if na and nb else 0
N=int(sys.argv[1]); res={}
for n,gr in enumerate(g,1):
    X=gr[0][1]; mem=[]
    for k,c,_,_ in gr:
        s=start_in_X(c,X); f=features(X,s,N); mem.append((k,s,f))
    pairs=[]
    for (k1,s1,f1),(k2,s2,f2) in itertools.combinations(mem,2):
        if f1.get('halt') or f2.get('halt'): pairs.append((k1,k2,None,None)); continue
        pairs.append((k1,k2,round(cos(f1['bag'],f2['bag']),3),round(abs(f1['exp']-f2['exp']),3)))
    res[n]={'members':[(k,s,None if f.get('halt') else {'exp':round(f['exp'],3),'left':round(f['left'],3),'width':f['width'],'top':sorted(f['bag'].items(),key=lambda x:-x[1])[:6]}) for k,s,f in mem],'pairs':pairs}
    print(n,[(k,s) for k,s,_ in mem],pairs,flush=True)
json.dump(res,open('regime.json','w'))
