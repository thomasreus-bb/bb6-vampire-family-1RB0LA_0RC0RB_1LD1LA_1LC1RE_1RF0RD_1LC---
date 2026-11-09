# build an msim state from a run-length list (cells from the head outward), head at the left end moving L in state q
from msim import Sim,BS,push
def rl_to_blocks(rl):
    out=[]; buf=[]
    def emit(blk,n):
        if out and out[-1][0]==blk: out[-1][1]+=n
        else: out.append([blk,n])
    for b,n in rl:
        while n>0 and buf:
            buf.append(b); n-=1
            if len(buf)==BS: emit(tuple(buf),1); buf=[]
        if n>=BS:
            emit((b,)*BS,n//BS); n%=BS
        buf+= [b]*n
        if len(buf)==BS: emit(tuple(buf),1); buf=[]
    if buf: emit(tuple(buf+[0]*(BS-len(buf))),1)
    return out
def make(rl,q):
    s=Sim(); blocks=rl_to_blocks(rl)
    s.R=[list(x) for x in reversed(blocks)]
    s.L=[]; s.q=q; s.d='L'; s.steps=0
    return s
