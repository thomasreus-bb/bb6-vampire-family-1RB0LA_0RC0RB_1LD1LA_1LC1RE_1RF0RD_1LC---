import re,sys
M='1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE'
T={}
for i,g in enumerate(M.split('_')):
    for b in (0,1):
        x=g[3*b:3*b+3]
        T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
def run(tape,q=2,maxs=10**7,stop=None):
    t=dict(enumerate(tape)); p=len(tape)-1; lo,hi=0,p
    for s in range(maxs):
        b=t.get(p,0); tr=T[(q,b)]
        if tr is None: return ('HALT',s)
        t[p]=tr[0]; p+=tr[1]; q=tr[2]
        if p>hi:
            hi=p
            if q==2:
                st=''.join(str(t.get(i,0)) for i in range(lo,hi+1))
                r=stop(st) if stop else None
                if r: return ('REC',s+1,st)
        if p<lo: lo=p
    return ('MAX',)
