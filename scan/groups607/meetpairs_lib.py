import itertools
S='ABCDEF'
def parse(t):
    d={}
    for i,g in enumerate(t.split('_')):
        for b in (0,1):
            x=g[3*b:3*b+3]; d[(S[i],b)]=None if x[0]=='-' else (x[0],x[1],x[2])
    return d
def code(d): return '_'.join(''.join('---' if d[(q,b)] is None else ''.join(d[(q,b)]) for b in (0,1)) for q in S)
def transform(d,P,mir):
    return {(P[q],b):(None if v is None else (v[0],({'L':'R','R':'L'}[v[1]] if mir else v[1]),P[v[2]])) for (q,b),v in d.items()}
def align(X,Y):
    dx=parse(X); dy=parse(Y)
    for mir in (0,1):
        for p in itertools.permutations(S):
            P=dict(zip(S,p)); t=transform(dy,P,mir)
            diff=[k for k in dx if dx[k]!=t[k]]
            if len(diff)==1: return code(t),P['A'],diff[0]
