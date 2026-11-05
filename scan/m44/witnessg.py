import sys
from collections import deque
import dfas
TM=sys.argv[1]; FAM=sys.argv[2]; ARGS=list(map(int,sys.argv[3].split(","))); LIM=int(sys.argv[4])
T=[[None if st[3*b+2]=='-' else (int(st[3*b]),1 if st[3*b+1]=='R' else -1,ord(st[3*b+2])-65) for b in range(2)] for st in TM.split('_')]
NQ,delta,lst=getattr(dfas,FAM)(*ARGS)
preds={}
for q in range(NQ):
    for c in (0,1): preds.setdefault(delta(q,c),[]).append((q,c))
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
tape={}; hpos=0; s=0
for i,(s_,h_,q_,stk) in enumerate(path):
    real_h=tape.get(hpos,0)
    # real DFA state of the real left half
    lo_=min(list(tape)+[hpos]); qr=0
    for k in range(lo_-2,hpos): qr=delta(qr,tape.get(k,0))
    if qr!=q_:
        print('DFA state differs at step',i,': abstract',lst[q_],' real',lst[qr]); lo=min(list(tape)+[hpos]); hi=max(list(tape)+[hpos])
        print('  real tape', ''.join(('['+str(tape.get(k,0))+']') if k==hpos else str(tape.get(k,0)) for k in range(lo,hi+1)), 'state','ABCDEF'[s])
        print('  previous step real tape', prevtape); break
    if (s_,h_)!=(s,real_h):
        print('diverges at step',i,'abstract',('ABCDEF'[s_],h_),'DFA state',lst[q_],'real',('ABCDEF'[s],real_h))
        lo=min(list(tape)+[hpos]); hi=max(list(tape)+[hpos]); print('real tape', ''.join(('['+str(tape.get(k,0))+']') if k==hpos else str(tape.get(k,0)) for k in range(lo,hi+1)))
        pq=path[i-1][2]; print('previous DFA state',lst[pq]); break
    if i==len(path)-1: print('no divergence?!'); break
    lo=min(list(tape)+[hpos]); hi=max(list(tape)+[hpos]); prevtape=''.join(('['+str(tape.get(k,0))+']') if k==hpos else str(tape.get(k,0)) for k in range(lo,hi+1))+' '+'ABCDEF'[s]
    w,d,s2=T[s][real_h]; tape[hpos]=w; hpos+=d; s=s2
