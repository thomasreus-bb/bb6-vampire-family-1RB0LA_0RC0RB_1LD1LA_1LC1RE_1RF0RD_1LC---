import sys; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from chain import Sim, parse
M=sys.argv[1] if len(sys.argv)>1 else '1RB0LE_1RC---_1RD1RE_1LA0RF_0RC0LA_0LC0RB'
NN=int(sys.argv[2]) if len(sys.argv)>2 else 400000
S=Sim(M); chk={}
while S.steps<NN and not S.halted:
    S.step()
    l,r=S.tape(); chk[S.steps]=(l.lstrip('0'), r.rstrip('0'), S.s, S.d)
T=parse(M); t={}; h=0; s=0; bad=0; ok=0; d=1
for n in range(1,NN+1):
    b=t.get(h,0); tr=T[s][b]
    if tr is None: break
    w,m,ns=tr; t[h]=w; h+=m; s=ns; d=m
    if n in chk:
        lo=min(min(t),h); hi=max(max(t),h)
        cut=h if d==1 else h+1
        L=''.join(str(t.get(x,0)) for x in range(lo,cut)).lstrip('0'); R=''.join(str(t.get(x,0)) for x in range(cut,hi+1)).rstrip('0')
        if chk[n]==(L,R,s,d): ok+=1
        else:
            bad+=1
            if bad<3: print('mismatch at',n,chk[n][2:],(s,d)); print(chk[n][0][-40:],'|',chk[n][1][:40]); print(L[-40:],'|',R[:40])
print('ok',ok,'bad',bad,'chainsteps',len(chk))
