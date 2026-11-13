# Pairs of the 607 holdouts whose tables differ in exactly one transition, up to renaming of the states and mirroring.
# For every machine and every transition slot, the slot is replaced by a wildcard and the table is put in a canonical form;
# two machines with the same key (and different values in the slot) differ in exactly that one transition.
import json,itertools,collections,sys
info={int(k):v for k,v in json.load(open('info607.json')).items()}
S='ABCDEF'
def parse(t):
    d={}
    for i,g in enumerate(t.split('_')):
        for b in (0,1):
            x=g[3*b:3*b+3]; d[(i,b)]=None if x[0]=='-' else (x[0],x[1],ord(x[2])-65)
    return d
PERMS=list(itertools.permutations(range(6)))
def keys(d):
    """for each slot (q,b): canonical key of the table with that slot wildcarded, plus the slot's value written in the same canonical naming"""
    res={}
    for mir in (0,1):
        for p in PERMS:
            inv=[0]*6
            for q in range(6): inv[p[q]]=q
            cells=[]
            for nq in range(6):
                q=inv[nq]
                for b in (0,1):
                    v=d[(q,b)]
                    cells.append('---' if v is None else v[0]+(('L' if v[1]=='R' else 'R') if mir else v[1])+S[p[v[2]]])
            for q in range(6):
                for b in (0,1):
                    i=2*p[q]+b
                    k=tuple(cells[:i])+('*',)+tuple(cells[i+1:])
                    old=res.get((q,b))
                    if old is None or k<old[0]: res[(q,b)]=(k,cells[i])
    return res
idx=collections.defaultdict(list)
for n,(k,(code,st,cls)) in enumerate(sorted(info.items())):
    d=parse(code)
    for (q,b),(key,val) in keys(d).items():
        idx[key].append((k,S[q]+str(b),val))
    if n%100==0: print(n,file=sys.stderr,flush=True)
pairs=[]
for key,lst in idx.items():
    for (k1,s1,v1),(k2,s2,v2) in itertools.combinations(lst,2):
        if v1!=v2 and k1!=k2: pairs.append((k1,s1,info[k1][0][7*'ABCDEF'.index(s1[0])+3*int(s1[1]):][:3],k2,s2,info[k2][0][7*'ABCDEF'.index(s2[0])+3*int(s2[1]):][:3]))
pairs=sorted(set(pairs))
json.dump(pairs,open('onediff.json','w'))
print(len(pairs),'pairs')
