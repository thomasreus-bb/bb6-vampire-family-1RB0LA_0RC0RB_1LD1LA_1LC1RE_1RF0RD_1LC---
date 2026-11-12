# abstract closure by sampling: start from the Bell class n = 4 mod 8 (as classes mod M), add all classes reached from random members
import sys,random,collections,pickle
from macro import step,run2
from segm import seg
M=int(sys.argv[1]); SAMP=int(sys.argv[2]); ROUNDS=int(sys.argv[3])
def cls(kind,p): return (kind,)+tuple(x%M for x in p)
rnd=random.Random(2)
S={('Bell',r) for r in range(4,M,8)}; frontier=set(S); halts=[]
def member(c):
    big=rnd.choice([3,40,300,5000,10**6,10**12])
    return tuple(r+M*rnd.randrange(1,big) for r in c[1:])
for rd in range(ROUNDS):
    new=set()
    for c in frontier:
        for _ in range(SAMP):
            p=member(c); k,q=seg(c[0],p)
            if k in('HALT','MAX'): halts.append((c,p)); continue
            d=cls(k,q)
            if d not in S: new.add(d)
    S|=new; frontier=new
    print('round',rd,'classes',len(S),'new',len(new),'halts',len(halts),flush=True)
    if not new: break
for h in halts[:6]: print('HALT',h)
pickle.dump(S,open('C%d.pkl'%M,'wb'))
print(dict(collections.Counter(c[0] for c in S)))
