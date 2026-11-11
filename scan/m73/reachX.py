# reachable tails of the common Bell system (start tail of no. 73) over all residue sequences, depth D, cap L cells
import pickle,glev2,markov,sys,collections
from gram73 import parse,runs
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
g=glev2.G2(M,'D','','110',2,3); g.TAB=pickle.load(open('tab73.pkl','rb'))
markov.LMAX=int(sys.argv[2])
starts=sys.argv[3].split(',') if len(sys.argv)>3 else ['1110111110110111']
front=set(starts); seen=set(front)
for d in range(int(sys.argv[1])):
    new=set()
    for W in front:
        for r in (0,1):
            e,W2=markov.entry_safe(g,r,W)
            if W2 is None:
                if e=='HALT': print('HALT',W,r); sys.exit()
                continue
            if W2 not in seen: seen.add(W2); new.add(W2)
    front=new
pickle.dump(g.TAB,open('tab73.pkl','wb'))
stat=collections.defaultdict(list); notG=[]
for W in seen:
    t=runs(W); p=parse(t)
    if p is None: notG.append(t); continue
    stat[len(p)-1].append(p)
print(len(seen),'reachable tails; not in G:',len(notG),notG[:3])
for nb in sorted(stat):
    L=stat[nb]
    ys=collections.Counter((p[-1][0],p[-1][1] if p[-1][1]<=12 else 'big') for p in L)
    print('blocks=%d: %d tails; Y: %s'%(nb,len(L),dict(ys)))
    if nb>=1:
        for pos in range(nb):
            v=[p[pos][1] for p in L]
            print('   block %d: types %s, chain min %d max %d'%(pos+1,dict(collections.Counter(p[pos][0] for p in L)),min(v),max(v)))
