import re,itertools,collections
S='ABCDEF'
s=open('scan/bell_candidates.md').read()
cands={}
for m in re.finditer(r'^## .*?\[(\d+)\]\(#t\d+\)\. `([^`]+)`',s,re.M):
    if 'entfernt' not in m.group(0): cands[int(m.group(1))]=m.group(2)
def T(code): return [code[7*i+3*b:7*i+3*b+3] for i in range(6) for b in (0,1)]
def forms(code):
    t=T(code); out=[]
    for mir in (0,1):
        for perm in itertools.permutations(range(6)):   # old state i -> new perm[i]
            new=[None]*12
            for i in range(6):
                for b in (0,1):
                    x=t[2*i+b]
                    y='---' if x[0]=='-' else x[0]+(x[1] if not mir else ('L' if x[1]=='R' else 'R'))+S[perm[S.index(x[2])]]
                    new[2*perm[i]+b]=y
            out.append((tuple(new),S[perm[0]],mir))
    return out
F={n:forms(c) for n,c in cands.items()}
base={n:tuple(T(c)) for n,c in cands.items()}
idx=collections.defaultdict(set)
pairs=list(itertools.combinations(range(12),2))
for n in cands:
    t=base[n]
    for (i,j) in pairs:
        idx[(i,j)+tuple(x for k,x in enumerate(t) if k not in (i,j))].add(n)
found={}
for n in cands:
    for f,st,mir in F[n]:
        for (i,j) in pairs:
            key=(i,j)+tuple(x for k,x in enumerate(f) if k not in (i,j))
            for m in idx.get(key,()):
                if m==n: continue
                d=sum(1 for k in range(12) if f[k]!=base[m][k])
                a,b=min(n,m),max(n,m)
                if (a,b) not in found or d<found[(a,b)][0]:
                    found[(a,b)]=(d,n,m,st,mir,[ (S[k//2]+str(k%2),base[m][k],f[k]) for k in range(12) if f[k]!=base[m][k]])
for (a,b),(d,n,m,st,mir,diffs) in sorted(found.items()):
    print('%3d %3d: %d different; no. %d renamed%s, started in %s, vs no. %d: %s'%(a,b,d,n,' and mirrored' if mir else '',st,m,diffs))
