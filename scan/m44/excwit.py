import sys
from collections import deque, defaultdict
import dfas
TM=sys.argv[1]; FAM=sys.argv[2]; ARGS=list(map(int,sys.argv[3].split(','))); LIM=int(sys.argv[4])
T=[[None if st[3*b+2]=='-' else (int(st[3*b]),1 if st[3*b+1]=='R' else -1,ord(st[3*b+2])-65) for b in range(2)] for st in TM.split('_')]
N0,d0,lst=getattr(dfas,FAM)(*ARGS); Q0=N0
delta=lambda q,c: d0(0,c) if q==Q0 else d0(q,c)
preds=defaultdict(list)
for q in range(N0+1):
    for c in (0,1): preds[delta(q,c)].append((q,c))
# config: (s,h,q,stack) ; stack = tuple of right cells (nearest first) followed by implicit U
starts=[(s,h,Q0,()) for s in (0,1,4) for h in (0,1)]
prev={c:None for c in starts}; dq=deque(starts); found=None
while dq:
    cfg=dq.popleft(); s,h,q,stk=cfg; tr=T[s][h]
    if tr is None: found=cfg; break
    w,d,s2=tr; nxt=[]
    if d==1:
        q2=delta(q,w)
        if stk: nxt.append((s2,stk[0],q2,stk[1:]))
        else: nxt += [(s2,c,q2,()) for c in (0,1)]
    else:
        if q==Q0 or len(stk)>=LIM: continue
        for (q1,c) in preds[q]: nxt.append((s2,c,q1,(w,)+stk))
    for n in nxt:
        if n not in prev: prev[n]=cfg; dq.append(n)
if not found: print('none'); sys.exit()
path=[]; c=found
while c: path.append(c); c=prev[c]
path.reverse(); print('witness length',len(path))
for (s,h,q,stk) in path: print('ABCDEF'[s],h,lst[q] if q!=Q0 else 'Q0',stk)
