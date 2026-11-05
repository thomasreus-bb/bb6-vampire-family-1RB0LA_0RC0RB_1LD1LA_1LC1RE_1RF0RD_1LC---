"""Find an abstract halting run (BFS, stack <= LIM) and follow it with concrete tapes: whenever the
abstract DFA state differs from the real left half, replace the left half by a shortest word with
that DFA state. Prints every replacement, so one sees which concrete configurations lead to HALT."""
import sys
from collections import deque
import dfas
TM=sys.argv[1]; FAM=sys.argv[2]; ARGS=list(map(int,sys.argv[3].split(','))); LIM=int(sys.argv[4])
T=[[None if st[3*b+2]=='-' else (int(st[3*b]),1 if st[3*b+1]=='R' else -1,ord(st[3*b+2])-65) for b in range(2)] for st in TM.split('_')]
NQ,delta,lst=getattr(dfas,FAM)(*ARGS)
preds={}
for q in range(NQ):
    for c in (0,1): preds.setdefault(delta(q,c),[]).append((q,c))
# shortest word for each DFA state
word={0:()}; dq=deque([0])
while dq:
    q=dq.popleft()
    for c in (0,1):
        n=delta(q,c)
        if n not in word: word[n]=word[q]+(c,); dq.append(n)
init=(0,0,0,()); prev={init:None}; dq=deque([init]); found=None
while dq:
    cfg=dq.popleft(); s,h,q,stk=cfg; tr=T[s][h]
    if tr is None: found=cfg; break
    w,d,s2=tr; nxt=[]
    if d==1: nxt.append((s2,stk[0] if stk else 0,delta(q,w),stk[1:]))
    else:
        if len(stk)>=LIM: continue
        st2=(w,)+stk
        if not any(st2): st2=()
        for (q1,c) in preds.get(q,[]): nxt.append((s2,c,q1,st2))
    for n in nxt:
        if n not in prev: prev[n]=cfg; dq.append(n)
if not found: print('no abstract halting run with stack <=',LIM); sys.exit()
path=[]; c=found
while c: path.append(c); c=prev[c]
path.reverse(); print('abstract halting run, length',len(path))
def show(left,h,right,s): return ''.join(map(str,left))+'['+str(h)+']'+''.join(map(str,right))+' '+'ABCDEF'[s]
for i,(s,h,q,stk) in enumerate(path):
    left=list(word[q]); right=list(stk)
    if i==0 or i==len(path)-1 or (i>0 and path[i-1][2]!=q and T[path[i-1][0]][path[i-1][1]][1]==-1):
        # print configurations right after a left move (where the DFA chooses)
        pass
    print('%4d %s   %s'%(i, show(left,h,right,s), lst[q]))
