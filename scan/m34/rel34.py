import itertools
def parse(s): return [[None if x[0]=='-' else (x[0],x[1],x[2]) for x in (r[:3],r[3:])] for r in s.split('_')]
def ren(t,perm,mir):
    # perm: old index -> new letter index
    n=[[None,None] for _ in range(6)]
    for i in range(6):
        for b in range(2):
            x=t[i][b]
            if x: d=x[1]; d={'L':'R','R':'L'}[d] if mir else d; x=(x[0],d,'ABCDEF'[perm['ABCDEF'.index(x[2])]])
            n[perm[i]][b]=x
    return n
s34='1RB1RC_1LC1LC_1RE0LD_1LB1RF_---1RA_0RD1RD'
s50='1RB1RB_1LC0RE_---1LD_0RA1LB_1RA1LF_0LE1LE'
t34,t50=parse(s34),parse(s50)
best=[]
for perm in itertools.permutations(range(6)):
    for mir in (0,1):
        n=ren(t34,perm,mir)
        d=[('ABCDEF'[i]+str(b),n[i][b],t50[i][b]) for i in range(6) for b in range(2) if n[i][b]!=t50[i][b]]
        if len(d)<=2: best.append((len(d),perm,mir,d))
for b in sorted(best): print(b[0],''.join('ABCDEF'[p] for p in b[1]),'mirror' if b[2] else '',b[3])
