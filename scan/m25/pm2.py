import sys
from pm import pm,fmt
n0=int(sys.argv[1])
for r in (0,1,2):
    n=n0+r; q=n//3
    for k in list(range(1,25))+[40,41,42,43,44,45]:
        st,out=pm(n,'0'+'1'*k)
        if out is None: print(r,k,st); continue
        o=fmt(out).split(' ',1)
        e=int(o[0][2:])-4*q
        print('r=%d k=%2d  e=%3d  T\'=%s'%(r,k,e,o[1] if len(o)>1 else 'e'))
