#!/usr/bin/env python3
"""Phase B of no. 41 as a sequence of segments. A segment starts at P1(1,b,c) and ends at the next
P1 start (new cascade step) or at phase A. Prints the segment types, their t=c/b ranges and the
affine maps (b,c) -> (b',c') resp. (x,y), fitted and checked exactly on all samples (mod-3 classes separate)."""
import sys; sys.set_int_max_str_digits(100000)
from fractions import Fraction as Fr
from collections import defaultdict
def segs(n):
    reg, s = 'Q', (2, n-1, 2); w=[]; out=[]; start=None
    while True:
        if reg=='P1':
            if start is not None: out.append((start,' '.join(w),('P1',s)))
            start=s; w=[]
            a,b,c=s; k=min(b,c-1); a,b,c=a+3*k,b-k,c-k
            if b==0: reg,s='P2',(a+3,0,c-4); w.append('d')
            else: reg,s='P3',(a+2,b-1,2); w.append('X')
        elif reg=='P2':
            a,b,c=s; ka=max(0,-(-(a-2)//3)); k=min(ka,c-1); a,b,c=a-3*k,b+2*k,c-k
            if a<=2:
                if a==0: reg,s='P1',(1,b+1,c-1); w.append('L0')
                elif a==1: reg,s='P1',(1,b+2,c-1); w.append('L1')
                else: out.append((start,' '.join(w),('A',(b+3,c-2)))); return out
            else: reg,s='Q',(a,b+1,2); w.append('Y')
        else:
            a,b,c=s; c+=2*b+2; s=(a-3,1,c) if reg=='P3' else (a-2,0,c); reg='P2'
def solve3(rows):
    # exact fit v = p*b + q*c + r from 3 independent rows, then check all
    import itertools
    for i,j,k in itertools.combinations(range(min(len(rows),40)),3):
        M=[[Fr(rows[t][0]),Fr(rows[t][1]),Fr(1),Fr(rows[t][2])] for t in (i,j,k)]
        # gaussian elimination
        try:
            for col in range(3):
                piv=next(r for r in range(col,3) if M[r][col]!=0); M[col],M[piv]=M[piv],M[col]
                for r in range(3):
                    if r!=col:
                        f=M[r][col]/M[col][col]; M[r]=[x-f*y for x,y in zip(M[r],M[col])]
            sol=[M[r][3]/M[r][r] for r in range(3)]
        except StopIteration: continue
        if all(sol[0]*b+sol[1]*c+sol[2]==v for b,c,v in rows): return sol
    return None
if __name__=='__main__':
    N=int(sys.argv[1]) if len(sys.argv)>1 else 1500
    data=defaultdict(list); n=28
    for i in range(N):
        for (a,b,c),w,res in segs(n):
            data[w].append((b,c,res))
            if res[0]=='A': x,y=res[1]; n=x+2*y+1
    def fmt(s):
        p,q,r=s; return '%s*b %+s*c %+s'%(p,q,r)
    for w,L in sorted(data.items(),key=lambda x:-len(x[1])):
        ts=[min(c*10**6//b,10**15)/10**6 for b,c,_ in L]
        line='%-28s %8d  t=c/b in [%.4f, %.4f]'%(w,len(L),min(ts),max(ts))
        maps=[]
        for m3 in range(3):
            sub=[(b,c,res) for b,c,res in L if (b-c)%3==m3]   # rounding class
            if not sub: continue
            if sub[0][2][0]=='P1':
                s1=solve3([(b,c,r[1][1]) for b,c,r in sub]); s2=solve3([(b,c,r[1][2]) for b,c,r in sub]); tgt="b',c'"
            else:
                s1=solve3([(b,c,r[1][0]) for b,c,r in sub]); s2=solve3([(b,c,r[1][1]) for b,c,r in sub]); tgt='x,y'
            maps.append('(b-c)%%3=%d: %s = %s ; %s'%(m3,tgt,fmt(s1) if s1 else '?',fmt(s2) if s2 else '?'))
        print(line); 
        for m in sorted(set(m.split(': ',1)[1] for m in maps)): print('     ',m, '' if len(set(x.split(': ',1)[1] for x in maps))==1 else '')
        if len(set(m.split(': ',1)[1] for m in maps))>1:
            for m in maps: print('        ',m)
