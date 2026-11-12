import collections,sys,pickle
from m41 import step_macro
N=int(sys.argv[1]); R={}
for kind,ar in (('P1',3),('P2',3),('P3',3),('Q',3),('A',2),('Bell',1)):
    rng=range(0,N+1)
    import itertools
    for p in itertools.product(rng,repeat=ar):
        if kind in('P1','P2','P3','Q') and p[2]==0: continue      # c >= 1 in the patterns
        if kind=='Q' and p[0]==0: continue
        R[(kind,p)]=step_macro(kind,p,200000)
pickle.dump(R,open('tab%d.pkl'%N,'wb'))
for kind in ('P1','P2','P3','Q','A','Bell'):
    G=collections.defaultdict(list)
    for (k,p),r in R.items():
        if k!=kind: continue
        if r[0] in('HALT','MAX'): G[(r[0],)].append(p)
        elif r[0]==kind: G[(r[0],tuple(x-y for x,y in zip(r[1],p)))].append(p)
        else: G[(r[0],'other')].append(p)
    print(kind)
    for key,ps in sorted(G.items(),key=lambda kv:-len(kv[1])):
        mn=tuple(min(p[i] for p in ps) for i in range(len(ps[0]))); mx=tuple(max(p[i] for p in ps) for i in range(len(ps[0])))
        print('   ->',key,len(ps),'min',mn,'max',mx, '' if len(ps)>6 else ps)
