#!/usr/bin/env python3
"""No. 44: can the machine halt while the head is inside the memory word r, for ANY content of r?
Excursion = the head enters r at its first cell from the left (in state s) and runs until it leaves r to the
left again.  pre* on the pushdown system:  stack = cells of r left of the head (exact, nearest on top),
bottom marker X = 'left end of r' (moving onto X = the excursion is over: no HALT);  the cells right of the
head are arbitrary: only a window of the last K cells pushed there is kept (beyond it: anything).
If no control (s, h, window) with stack [X] can reach HALT, no excursion can ever halt, whatever r is."""
import sys
from collections import defaultdict, deque
TM=sys.argv[1]; K=int(sys.argv[2])
T=[[None if st[3*b+2]=='-' else (int(st[3*b]),1 if st[3*b+1]=='R' else -1,ord(st[3*b+2])-65) for b in range(2)] for st in TM.split('_')]
NQ=1<<K
# right part (cells right of the head), window of the nearest K cells: state w, bit 0 = nearest
def push_right(q,c): return ((q<<1)|c)&(NQ-1)              # head moves left: old head cell becomes nearest right cell
def pop_right(q):                                            # head moves right: reads nearest right cell = q&1, rest shifts, new far bit unknown
    c=q&1; base=q>>1
    return c,[base|(x<<(K-1)) for x in (0,1)]
ctl=lambda s,h,q:(s*2+h)*NQ+q
X=2; SYM=(0,1,2); F='F'
trans=defaultdict(set); work=deque()
def add(p,g,q):
    if q not in trans[(p,g)]: trans[(p,g)].add(q); work.append((p,g,q))
rules1=defaultdict(list); rules2=defaultdict(list)
for g in SYM: add(F,g,F)
for s in range(6):
    for h in (0,1):
        tr=T[s][h]
        for q in range(NQ):
            p=ctl(s,h,q)
            if tr is None:
                for g in SYM: add(p,g,F)
                continue
            w,d,s2=tr
            if d==1:   # move right: push w on the left stack, read the nearest right cell
                c,qs=pop_right(q)
                for q2 in qs:
                    for g in SYM: rules2[(ctl(s2,c,q2),w)].append((p,g,g))     # (p,g) -> (p2, w g)
            else:      # move left: pop the top of the left stack (X = exit, no rule = no HALT)
                q2=push_right(q,w)
                for g in (0,1): add(p,g,ctl(s2,g,q2))                       # (p,g) -> (p2, eps)
while work:
    p2,g2,q=work.popleft()
    for (p,g) in rules1.get((p2,g2),()): add(p,g,q)
    for (p,g,g3) in rules2.get((p2,g2),()):
        for q3 in list(trans[(q,g3)]): add(p,g,q3)
        rules1[(q,g3)].append((p,g))
bad=[]
for s in range(6):
    for h in (0,1):
        for q in range(NQ):
            if F in trans.get((ctl(s,h,q),X),()): bad.append(('ABCDEF'[s],h,q))
ent=[b for b in bad if b[0] in 'ABE']
print('K=%d: start controls (head on the first cell of r, any content) that can reach HALT:'%K,len(bad),' of them with entry state A/B/E:',len(ent), ent[:6])
