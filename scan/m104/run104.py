# long run of DeepMind's map for no. 104; HALT happens when a scan reaches the end of the stack with only odd digits.
# Reports: stack length, sum of digits (tape length), how often a scan reached the end (near misses), and the longest scan.
import sys,time
from dm104 import step
N=int(sys.argv[1]); st=(0,[0]); t0=time.time(); ends=0; longest=0
for k in range(1,N+1):
    d,R=st
    # length of the odd prefix of d::R (what the scan will pass)
    L=0
    if d%2:
        L=1
        for e in R:
            if e%2: L+=1
            else: break
    if L>=len(R)+1 and d%2==0: pass
    longest=max(longest,L)
    if L==len(R)+1: print('HALT at macro step',k); break
    if d%2==1 and L==len(R): ends+=1      # scan reaches the end, last value even -> near miss
    st=step(d,R)
    if st is None: print('HALT (map) at',k); break
    if k%(N//10)==0:
        d,R=st
        print(k,'stack length',len(R)+1,'tape about',sum(R)+d+len(R),'cells; scans to the end',ends,'; longest odd run',longest,'; %.0f s'%(time.time()-t0),flush=True)
