import itertools,sys,collections
def parse(M):
    rows=M.split("_"); T=[]
    for s in rows:
        T.append([None if s[3*b]=='-' else (s[3*b],s[3*b+1],ord(s[3*b+2])-65) for b in range(2)])
    return T
def transform(T,perm,mirror):
    # perm: old state -> new state
    n=len(T); U=[None]*n
    for s in range(n):
        row=[]
        for b in range(2):
            t=T[s][b]
            if t is None: row.append("---")
            else:
                d=t[1]
                if mirror: d={'L':'R','R':'L'}[d]
                row.append(t[0]+d+chr(65+perm[t[2]]))
        U[perm[s]]="".join(row)
    return "_".join(U)
def canon(M):
    T=parse(M); best=None
    for perm in itertools.permutations(range(len(T))):
        for mir in (0,1):
            c=transform(T,perm,mir)
            if best is None or c<best[0]: best=(c,perm,mir)
    return best
L=[l.split()[1] for l in open(sys.argv[1]) if not l.startswith("#")]
G=collections.defaultdict(list)
for i,M in enumerate(L):
    c,perm,mir=canon(M); G[c].append((i+1,M,perm,mir))
for c,v in G.items():
    if len(v)>1: print("same table up to renaming/mirroring:",[(i,M) for i,M,_,_ in v])
# near-isomorphic: canonical forms that differ in exactly one transition (compare all transforms)
def diff1(A,B):
    a=A.split("_"); b=B.split("_"); d=sum(x[0:3]!=y[0:3] for r1,r2 in zip(a,b) for x,y in ((r1[:3],r2[:3]),(r1[3:],r2[3:])))
    return d
near=[]
cs=[(i+1,M) for i,M in enumerate(L)]
T2={i:parse(M) for i,M in cs}
for (i,A),(j,B) in itertools.combinations(cs,2):
    TA=parse(A); best=13
    for perm in itertools.permutations(range(6)):
        for mir in (0,1):
            d=diff1(transform(TA,perm,mir),B)
            if d<best: best=d
    if best<=2: near.append((best,i,j,A,B))
for x in sorted(near): print("differ in %d transition(s): no. %d %s  ~  no. %d %s"%(x[0],x[1],x[3],x[2],x[4]))
