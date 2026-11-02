# follow the tail counter of no. 39: one Bell from [0] P 1^N T with large N, read the new tail
import sys,re
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','m95'))
import fast
from chain import Sim
fast.REPORT_STATE=2
M='1RB1LC_1LC0RF_0LF1LD_0LE---_1RF1LC_1LE0RA'
class Done(Exception): pass
USE2=True
def bell(P,N,tail):
    S=Sim(M); S.s=2; S.d=1
    seq=[['0',1]]+[[c,1] for c in P]+[['1',N]]
    for m in tail: seq+= [['0',1],['1',m]] if m>0 else [['0',1]]
    seq+=[['0',1],['1',2]]
    S.side[1].runs=[list(x) for x in reversed(seq)]
    res={}
    def rep(S,out):
        pos=0; best=None
        for w,c in out:
            L=len(w)*c
            if set(w)=={'1'} and (best is None or L>best[1]): best=(pos,L)
            pos+=L
        if best and best[0]<=4 and best[1]>N:
            res['out']=out; raise Done
    try: (fast.run2 if USE2 else fast.run)(M,10**400,9,rep,S0=S)
    except Done: pass
    if S.halted: return ('HALT',S.steps)
    out=res['out']
    s=''.join(w*c for w,c in out if len(w)*c<10**6) # small parts only
    # parse: P' = cells before big run; tail = runs of ones after
    i=0; toks=[]
    for w,c in out: toks.append((w,c))
    # expand into list of (bit,count) runs
    runs=[]
    for w,c in toks:
        if len(w)==1: runs.append([w,c])
        else:
            for ch in w*c if len(w)*c<10**6 else None: runs.append([ch,1])
    merged=[]
    for b,c in runs:
        if merged and merged[-1][0]==b: merged[-1][1]+=c
        else: merged.append([b,c])
    k=max(range(len(merged)),key=lambda j: merged[j][1] if merged[j][0]=='1' else -1)
    Pp=''.join(b*c for b,c in merged[:k]).lstrip('0')
    Np=merged[k][1]
    rest=merged[k+1:]
    ones=[c for b,c in rest if b=='1']
    return (Pp,Np,ones,S.steps)
if __name__=='__main__':
    N0=int(sys.argv[1]) if len(sys.argv)>1 else 10**30
    tail=[8]; P=''
    for stage in range(int(sys.argv[2]) if len(sys.argv)>2 else 12):
        for r in (1,):
            N=N0+((r-N0)%4)
            out=bell(P,N,tail)
            print('stage',stage,'tail',tail,'N%4',r,'->',out[0] if out[0]=='HALT' else ('P=%r N\'-1.5N=%d tail=%s'%(out[0],out[1]-3*N//2,out[2])),flush=True)
        if out[0]=='HALT': break
        tail=out[2][:-1] if out[2] and out[2][-1]==2 else out[2]
