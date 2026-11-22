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
s34='1RB1LE_0LC0LB_1RD1LC_1RD1RA_1RF0LA_---1RE'
s50='1RB1LC_1RC0RF_1RD0LB_1RE0LD_1LF---_0RA1LA'
t34,t50=parse(s34),parse(s50)
best=[]
for perm in itertools.permutations(range(6)):
    for mir in (0,1):
        n=ren(t34,perm,mir)
        d=[('ABCDEF'[i]+str(b),n[i][b],t50[i][b]) for i in range(6) for b in range(2) if n[i][b]!=t50[i][b]]
        if len(d)<=12: best.append((len(d),perm,mir,d))
for b in sorted(best): print(b[0],''.join('ABCDEF'[p] for p in b[1]),'mirror' if b[2] else '',b[3])
