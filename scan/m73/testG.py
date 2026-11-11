# closure test of the family G under the exact level map (both residues), random members
import random,sys,collections,pickle,glev2
from gram73 import parse,runs,word
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
g=glev2.G2(M,'D','','110',2,3)
g.TAB=pickle.load(open('tab73.pkl','rb'))
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2]); JM=int(sys.argv[3]); KM=int(sys.argv[4]); BM=int(sys.argv[5])
c=collections.Counter(); bad=[]
def member():
    t=[]
    for _ in range(rnd.randrange(0,BM+1)):
        j=rnd.randrange(1,JM+1)
        t+= ([3,5] if rnd.random()<0.5 else [8])+[2]*j
    if rnd.random()<0.5: t+=[3*rnd.randrange(1,KM//3+1)]
    else: t+=[3,3*rnd.randrange(2,KM//3+1)]
    return t
for i in range(T):
    t=member(); W=word(t)
    for r in (0,1):
        try: e,W2=g.entry(r,W)
        except RuntimeError as ex:
            c['HALT' if 'HALT' in str(ex) else 'ERR']+=1; bad.append((r,t,str(ex)[:80])); continue
        ok=parse(runs(W2)) is not None
        c['in G' if ok else 'NOT in G']+=1
        if not ok: bad.append((r,t,runs(W2)[:20]))
print(dict(c))
for b in bad[:15]: print(b)
pickle.dump(g.TAB,open('tab73.pkl','wb'))
