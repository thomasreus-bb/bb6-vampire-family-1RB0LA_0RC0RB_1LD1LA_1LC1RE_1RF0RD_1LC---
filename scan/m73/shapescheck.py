import random,sys,pickle
sys.argv=[sys.argv[0]]+sys.argv[1:]
import shapes73_lib as L
from gram73 import runs,word
L.rnd=random.Random(int(sys.argv[1])); REP=int(sys.argv[2])
S=pickle.load(open('shapes73.pkl','rb')); new=set(); halts=[]; n=0
for sh in sorted(S):
    for k in range(REP):
        JM=L.rnd.choice([3,5,12,30,50]); KM=L.rnd.choice([40,90,200,300])
        t=L.concrete(sh,JM,KM); W=word(t)
        for r in (0,1):
            e,W2=L.markov.entry_safe(L.g,r,W); n+=1
            if W2 is None:
                if e=='HALT': halts.append((sh,t,r))
                continue
            s2=L.shape(runs(W2))
            if s2 not in S: new.add(s2)
print('checked',n,'levels; new shapes',len(new),'halts',len(halts))
for x in list(new)[:10]: print('.'.join(x))
pickle.dump(L.g.TAB,open('tab73.pkl','wb'))
