# closure test of the refined family G1: X* Y with (number of blocks >= 2 => Y in {[3],[3,6]})
import random,sys,collections,pickle,glev2
from gram73 import parse,runs,word
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
g=glev2.G2(M,'D','','110',2,3); g.TAB=pickle.load(open('tab73.pkl','rb'))
def inG1(t):
    p=parse(t)
    if p is None: return False
    nb=len(p)-1; y=p[-1]
    return nb<=1 or y in (('Y',3),('Y3',6))
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2]); JM=int(sys.argv[3]); KM=int(sys.argv[4]); BM=int(sys.argv[5])
c=collections.Counter(); bad=[]
for i in range(T):
    nb=rnd.randrange(0,BM+1); t=[]
    for _ in range(nb): t+=([3,5] if rnd.random()<0.5 else [8])+[2]*rnd.randrange(1,JM+1)
    if nb>=2: t+= [3] if rnd.random()<0.5 else [3,6]
    else: t+= [3*rnd.randrange(1,KM//3+1)] if rnd.random()<0.5 else [3,3*rnd.randrange(2,KM//3+1)]
    W=word(t)
    for r in (0,1):
        try: e,W2=g.entry(r,W)
        except RuntimeError as ex:
            c['HALT' if 'HALT' in str(ex) else 'ERR']+=1; bad.append((r,t,str(ex)[:60])); continue
        ok=inG1(runs(W2)); c['in G1' if ok else 'NOT in G1']+=1
        if not ok: bad.append((r,t,runs(W2)[:24]))
print(dict(c))
for b in bad[:12]: print(b)
pickle.dump(g.TAB,open('tab73.pkl','wb'))
