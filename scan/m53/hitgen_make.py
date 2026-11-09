import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import build
from msim import BS
def make2(rl,q):
    # like build.make but supports periodic units
    blocks=[]; buf=[]
    def emit(blk,n):
        if blocks and blocks[-1][0]==blk: blocks[-1][1]+=n
        else: blocks.append([blk,n])
    def push_cells(cells):
        nonlocal buf
        for c in cells:
            buf.append(c)
            if len(buf)==BS: emit(tuple(buf),1); buf=[]
    for x in rl:
        if x[0]=='U':
            u=[int(c) for c in x[1]]; k=x[2]; n=k*len(u)
            # fill buffer with whole cells until aligned, then bulk blocks, then remainder
            i=0
            while buf and n>0: push_cells([u[i%len(u)]]); i+=1; n-=1
            if n>=BS:
                blk=tuple(u[(i+j)%len(u)] for j in range(BS)); m=n//BS; emit(blk,m)
                i+=m*BS; n-=m*BS
            while n>0: push_cells([u[i%len(u)]]); i+=1; n-=1
        else:
            b,n=x
            while buf and n>0: push_cells([b]); n-=1
            if n>=BS: emit((b,)*BS,n//BS); n%=BS
            push_cells([b]*n)
    if buf: emit(tuple(buf+[0]*(BS-len(buf))),1)
    s=build.Sim(); s.R=[list(x) for x in reversed(blocks)]; s.L=[]; s.q=q; s.d='L'; s.steps=0
    return s
