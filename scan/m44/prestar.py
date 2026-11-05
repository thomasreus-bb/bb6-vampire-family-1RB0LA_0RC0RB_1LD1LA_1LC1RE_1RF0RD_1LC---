#!/usr/bin/env python3
"""pre* saturation (Bouajjani, Esparza, Maler) for a 2-symbol TM seen as a pushdown system.
Stack = right half of the tape (nearest cell on top) over {0,1}, bottom symbol Z = 'all zeros from here on'.
Left half = only the state of a DFA that reads it from the far (all-zero) end towards the head.
Control = (TM state, head symbol, DFA state).
  move R writing w: q -> delta(q,w); the head reads the popped top (from Z it reads 0 and Z stays)
  move L writing w: w is pushed; the head reads the nearest left cell c, for every q' with delta(q',c) = q
pre* of the halting configurations is a P-automaton; if the start configuration is not accepted,
the abstract system (which over-approximates the TM) cannot halt, hence the TM never halts.
DFA: given as a module with NQ, q0, delta(q,c) (q0 must satisfy delta(q0,0) == q0)."""
import sys
from collections import defaultdict, deque
def prestar(TM, NQ, delta, verbose=False):
    T=[[None if st[3*b+2]=='-' else (int(st[3*b]),1 if st[3*b+1]=='R' else -1,ord(st[3*b+2])-65) for b in range(2)] for st in TM.split('_')]
    preds=defaultdict(list)
    for q in range(NQ):
        for c in (0,1): preds[delta(q,c)].append((q,c))
    ctl=lambda s,h,q: (s*2+h)*NQ+q
    NC=12*NQ; F=NC; Z=2; SYM=(0,1,2)
    trans=defaultdict(set); work=deque()
    def add(p,g,q):
        if q not in trans[(p,g)]: trans[(p,g)].add(q); work.append((p,g,q))
    rules1=defaultdict(list)   # (p2,g2) -> [(p,g)]      meaning (p,g) -> (p2,g2)
    rules2=defaultdict(list)   # (p2,g2) -> [(p,g,g3)]   meaning (p,g) -> (p2,g2 g3)
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
                    for g in (0,1): add(p,g,ctl(s2,g,q2))
                    rules1[(ctl(s2,0,q2),Z)].append((p,Z))
                else:
                    for (q1,c) in preds[q]:
                        for g in SYM: rules2[(ctl(s2,c,q1),w)].append((p,g,g))
    n=0
    while work:
        p2,g2,q=work.popleft(); n+=1
        for (p,g) in rules1.get((p2,g2),()): add(p,g,q)
        for (p,g,g3) in rules2.get((p2,g2),()):
            for q3 in list(trans[(q,g3)]): add(p,g,q3)
            rules1[(q,g3)].append((p,g))
    return trans, ctl, F
def accepts(trans, start, stack, F):
    cur={start}
    for g in stack: cur={q for p in cur for q in trans.get((p,g),())}
    return F in cur
if __name__=='__main__':
    TM=sys.argv[1]; K=int(sys.argv[2])
    NQ=1<<K
    delta=lambda q,c: ((q<<1)|c)&(NQ-1)
    trans,ctl,F=prestar(TM,NQ,delta)
    start=ctl(0,0,0)     # state A, head on 0, left half all zeros (window 0^K = state 0)
    print('K=%d: blank start accepted by pre*(HALT):'%K, accepts(trans,start,[2],F), ' transitions:',sum(len(v) for v in trans.values()))
