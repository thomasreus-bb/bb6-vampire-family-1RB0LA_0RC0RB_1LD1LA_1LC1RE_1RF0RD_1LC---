# Macro orbit of no. 42 from the blank tape, with the exact rules R1-R4 and direct simulation (ev42) for merges M(c,e) with c even.
import sys,time,math
from rules42 import X2,batch
def step(ev):
    t,x,y=ev
    if t=='X':
        if y>=3:   # jump over all R1 steps
            if y%2==0: return ('X',x+y-2,2),'R1*'
            return ('X',x+y-1,1),'R1*'
        if y==1: return ('X',1,2*x+6),'R2'
        if y==2: return X2(x),'R3'
    if t=='Z': return ('M',x,y),'Z'
    if t=='M':
        if x%2==1: return (('X',x+6,y-1) if y>=2 else X2(x+4)),'R4'
        r=batch([ev])[0]
        return r,'merge even'
    return None,'?'
ev=('X',1,4)   # first event from the blank tape: 0 1 0 1^4 at step 6
n=0; merges=[]; t0=time.time(); lim=float(sys.argv[1])
while time.time()-t0<lim:
    nx,how=step(ev); n+=1
    if how!='R1*': print(n,how,ev,'->',nx,flush=True)
    if how=='merge even':
        merges.append((ev[1],ev[2],nx)); print(n,'merge even: c=%d e=%d -> %s'%(ev[1],ev[2],nx),flush=True)
    if nx is None or nx[0] not in 'XZM':
        print('stop:',ev,'->',nx); break
    ev=nx
print('macro events',n,'last',ev[0],'sizes ~10^%.1f'%math.log10(max(ev[1],ev[2],1)))
