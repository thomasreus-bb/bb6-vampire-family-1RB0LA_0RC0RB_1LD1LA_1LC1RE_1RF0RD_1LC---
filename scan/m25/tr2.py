import sys
exec(open('comp.py').read().split('for l in sys.stdin')[0])
M='1RB0LE_1LC0RD_0RA1LD_0LC1RA_1LF1LA_---1LA'
T={}
for i,s in enumerate(M.split('_')):
    for b in range(2):
        x=s[3*b:3*b+3]
        T[(chr(65+i),b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,x[2])
def run(tape,q,n,every=None):
    t=dict(enumerate(tape)); pos=-1; lastd=None
    for s in range(n):
        b=t.get(pos,0); r=T[(q,b)]
        if r is None: print('HALT',s); return
        t[pos]=r[0]; pos+=r[1]; q=r[2]
        if r[1]!=lastd:
            lo=min(min(t),pos);hi=max(max(t),pos)
            L=''.join(str(t.get(i,0)) for i in range(lo,pos)).lstrip('0'); R=''.join(str(t.get(i,0)) for i in range(pos,hi+1)).rstrip('0')
            print(s+1,'%s %s%s %s'%(comp(L) if L else '.', q, '>' if r[1]>0 else '<', comp(R) if R else '.'))
        lastd=r[1]
tape=[int(c) for c in sys.argv[1]]; run(tape,sys.argv[2],int(sys.argv[3]))
