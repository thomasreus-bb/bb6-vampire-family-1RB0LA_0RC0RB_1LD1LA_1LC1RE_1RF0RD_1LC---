# Abstract simulation (sound over-approximation) for nos. 27 and 29.
# Tape = left segments | head cell | right segments, blank (0) beyond both ends.
# A segment is (symbol, length); a length is exact (1..K-1) or ('L', r) = "at least K and = r mod 3".
# Every concrete configuration is represented by at least one abstract configuration, and every concrete step
# is matched by an abstract step (taking a cell from a long segment may leave a long one or the exact K-1).
# If the set of abstract configurations reachable from the blank tape is finite and contains no halting
# configuration, the machine never halts.
# usage: python3 absim.py TM K [maxstates] [maxsegs]
import sys
from collections import deque
TM=sys.argv[1]; K=int(sys.argv[2]); MAXS=int(sys.argv[3]) if len(sys.argv)>3 else 2000000
MAXSEG=int(sys.argv[4]) if len(sys.argv)>4 else 40
S='ABCDEF'; T={}
for i,g in enumerate(TM.split('_')):
    for b in (0,1):
        x=g[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,S.index(x[2]))
M=int(sys.argv[5]) if len(sys.argv)>5 else 3
def inc(L):
    if L=='?': return '?'
    if isinstance(L,tuple): return ('L',(L[1]+1)%M)
    return L+1 if L+1<K else ('L',(L+1)%M)
def decs(L):
    """possible lengths after removing one cell (0 means the segment disappears)"""
    if isinstance(L,tuple):
        r=L[1]; out=[('L',(r-1)%M)]
        if K%M==r: out.append(K-1)
        return out
    return [L-1]
def push(segs,sym):
    """add one cell with symbol sym at the inner end of a segment list (inner end = last element)"""
    if segs and segs[-1][0]==sym: return segs[:-1]+((sym,inc(segs[-1][1])),)
    return segs+((sym,1),)
def pops(segs):
    """take one cell from the inner end: list of (symbol, remaining segs)"""
    if not segs: return [(0,segs)]
    sym,L=segs[-1]; out=[]
    for L2 in decs(L):
        rest=segs[:-1] if L2==0 else segs[:-1]+((sym,L2),)
        out.append((sym,rest))
    return out
def norm(segs):
    # outer end (index 0) must not be a 0-segment (it merges with the blank)
    while segs and segs[0][0]==0: segs=segs[1:]
    return segs
start=((),0,0,())   # left segs (outer..inner), state, head symbol, right segs (outer..inner)
seen={start}; dq=deque([start]); halts=[]; maxseg=0
while dq:
    left,q,h,right=dq.popleft()
    tr=T[(q,h)]
    if tr is None: halts.append((left,q,h,right));
    if tr is None:
        if len(halts)>3: break
        continue
    w,d,q2=tr
    if d==1:
        nl=push(left,w); cand=[(nl,q2,s,r) for s,r in pops(right)]
    else:
        nr=push(right,w); cand=[(l,q2,s,nr) for s,l in pops(left)]
    for l,qq,s,r in cand:
        c=(norm(l),qq,s,norm(r))
        if c not in seen:
            n=len(c[0])+len(c[3]); maxseg=max(maxseg,n)
            if n>MAXSEG: print('too many segments',n); sys.exit(1)
            seen.add(c); dq.append(c)
            if len(seen)>MAXS: print('too many states', len(seen)); sys.exit(1)
def show(c):
    l,q,h,r=c
    f=lambda segs: ' '.join('%d^%s'%(s,(L if not isinstance(L,tuple) else '≥%d≡%d(%d)'%(K,L[1],M))) for s,L in segs)
    return '%s [%s%d] %s'%(f(l),S[q],h,f(tuple(reversed(r))))
print('K=%d: %d abstract configurations, max %d segments, halting reachable: %d'%(K,len(seen),maxseg,len(halts)))
for c in halts[:4]: print('  HALT:',show(c))
