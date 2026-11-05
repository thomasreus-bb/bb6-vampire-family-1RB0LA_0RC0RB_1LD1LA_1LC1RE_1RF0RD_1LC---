#!/usr/bin/env python3
"""No. 44: can the machine halt while the head is inside the memory word r, for ANY content of r?
Pushdown model of one excursion (the head enters r at its first cell, runs until it leaves r to the left):
  stack = cells RIGHT of the head (exact, nearest on top), bottom U = unread part of r (arbitrary content:
          popping U gives 0 or 1, U stays);
  DFA   = the cells of r LEFT of the head (written by the machine), read from the left end of r;
          the special DFA state q0 = 'nothing left of the head': a move left from q0 leaves r (no HALT).
If no start control (s in {A,B,E}, any head cell, q0) with stack [U] reaches HALT, no excursion can halt.
DFA: family from dfas.py, with a new start state q0 placed in front."""
import sys
from collections import defaultdict, deque
import dfas
TM=sys.argv[1]; FAM=sys.argv[2]; ARGS=list(map(int,sys.argv[3].split(',')))
T=[[None if st[3*b+2]=='-' else (int(st[3*b]),1 if st[3*b+1]=='R' else -1,ord(st[3*b+2])-65) for b in range(2)] for st in TM.split('_')]
N0,d0,lst=getattr(dfas,FAM)(*ARGS)
NQ=N0+1; Q0=N0
def delta(q,c): return d0(0,c) if q==Q0 else d0(q,c)
preds=defaultdict(list)
for q in range(NQ):
    for c in (0,1): preds[delta(q,c)].append((q,c))
ctl=lambda s,h,q:(s*2+h)*NQ+q
U=2; SYM=(0,1,2); F='F'
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
            if d==1:
                q2=delta(q,w)
                for g in (0,1): add(p,g,ctl(s2,g,q2))                 # pop the nearest right cell
                for c in (0,1): rules1[(ctl(s2,c,q2),U)].append((p,U)) # unread cell: arbitrary, U stays
            else:
                if q==Q0: continue                                     # leaves r: excursion over
                for (q1,c) in preds[q]:
                    for g in SYM: rules2[(ctl(s2,c,q1),w)].append((p,g,g))
while work:
    p2,g2,q=work.popleft()
    for (p,g) in rules1.get((p2,g2),()): add(p,g,q)
    for (p,g,g3) in rules2.get((p2,g2),()):
        for q3 in list(trans[(q,g3)]): add(p,g,q3)
        rules1[(q,g3)].append((p,g))
bad=[('ABCDEF'[s],h) for s in range(6) for h in (0,1) if F in trans.get((ctl(s,h,Q0),U),())]
print(FAM,ARGS,'NQ=%d'%NQ,' start controls (entry state, first cell) that can reach HALT:',bad)
