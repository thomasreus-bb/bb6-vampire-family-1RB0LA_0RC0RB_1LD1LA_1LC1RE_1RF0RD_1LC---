# shortest residue path from the real start tail to a halting entry, and a concrete n that follows it
import glev,pickle,collections,markov
g=glev.G('1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD','A','001110',3,4)
g.TAB=pickle.load(open('tab105.pkl','rb'))
start='011'; par={start:None}; q=collections.deque([start]); goal=None
while q:
    W=q.popleft()
    for r in range(3):
        e,W2=markov.entry_safe(g,r,W)
        if W2 is None:
            if e=='HALT': goal=(W,r); q.clear(); break
            continue
        if W2 not in par: par[W2]=(W,r,e); q.append(W2)
W,r=goal; path=[r]; tails=[W]
while par[W] is not None:
    W,rr,e=par[W]; path.append(rr); tails.append(W)
path.reverse(); tails.reverse()
print('levels to HALT',len(path),'residues',''.join(map(str,path)))
print('tails', ' -> '.join('.'.join(map(str,glev.tails(t))) or 'e' for t in tails))
