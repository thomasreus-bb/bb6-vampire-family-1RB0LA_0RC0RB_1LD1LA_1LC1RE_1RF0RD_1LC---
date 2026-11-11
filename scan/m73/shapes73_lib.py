# shape closure for the common Bell system of nos. 72/73/97.
# shape: runs of the tail with chains of >= 2 twos as '2*', values >= 12 as 'K<r mod 3>', smaller values exact.
# Each shape is concretized with random parameters; successors (both residues) are mapped back to shapes; repeat.
import random,sys,pickle,collections,glev2,markov
from gram73 import runs,word
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
g=glev2.G2(M,'D','','110',2,3); g.TAB=pickle.load(open('tab73.pkl','rb'))
markov.LMAX=6000
rnd=random.Random(1)
def shape(t):
    out=[];i=0
    while i<len(t):
        if t[i]==2:
            j=i
            while j<len(t) and t[j]==2: j+=1
            out.append('2' if j-i==1 else '2*'); i=j; continue
        out.append(str(t[i]) if t[i]<12 else 'K%d'%(t[i]%3)); i+=1
    return tuple(out)
def concrete(sh,JM,KM):
    t=[]
    for x in sh:
        if x=='2*': t+=[2]*rnd.randrange(2,JM)
        elif x.startswith('K'): r=int(x[1]); t.append(3*rnd.randrange(4,KM//3)+r)
        else: t.append(int(x))
    return t
