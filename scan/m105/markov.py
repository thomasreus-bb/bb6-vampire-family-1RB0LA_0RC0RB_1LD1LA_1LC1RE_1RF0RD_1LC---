# halting rate per level under random residues (each r with probability 1/m), Markov chain over tails with pruning
import glev,glev2,pickle,sys,collections,math
LMAX=int(sys.argv[4]) if len(sys.argv)>4 else 4000
def entry_safe(g,r,W):
    key=(r,W)
    if key in g.TAB: return g.TAB[key]
    if len(W)>LMAX: return ('BIG',None)
    try: return g.entry(r,W)
    except RuntimeError as ex:
        if 'HALT' in str(ex): g.TAB[key]=('HALT',None); return g.TAB[key]
        raise
def rate(g,W0,steps,prune):
    dist={W0:1.0}; out=[]; big=[0.0]
    for t in range(steps):
        new=collections.defaultdict(float); h=0.0
        for W,p in dist.items():
            for r in range(g.m):
                e,W2=entry_safe(g,r,W)
                if W2 is None:
                    if e=='BIG': big[0]+=p/g.m
                    else: h+=p/g.m
                else: new[W2]+=p/g.m
        dist={W:p for W,p in new.items() if p>prune}
        out.append(h)
        if t%10==0 or t==steps-1: print('level',t,'halt mass this level %.3e'%h,'states',len(dist),'kept mass %.6f'%sum(dist.values()),'too long (total) %.3e'%big[0],flush=True)
    return out
if __name__=='__main__':
    which=sys.argv[1]; steps=int(sys.argv[2]); prune=float(sys.argv[3])
    if which=='105':
        g=glev.G('1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD','A','001110',3,4); W0='011'; tf='tab105.pkl'
    else:
        M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
        g=glev2.G2(M,'D','','110',2,3); W0='1110111110110111'; tf='tab73.pkl'
    try: g.TAB=pickle.load(open(tf,'rb'))
    except Exception: pass
    rate(g,W0,steps,prune)
    pickle.dump(g.TAB,open(tf,'wb'))
