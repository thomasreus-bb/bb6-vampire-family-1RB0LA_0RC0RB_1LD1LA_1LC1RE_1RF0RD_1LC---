# fast simulation of no. 39 (uses ../m95/chain.py and fast.py); prints the configuration at each Bell start (state C, head at the left end)
import sys,time
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','m95'))
import fast
fast.REPORT_STATE=2
M='1RB1LC_1LC0RF_0LF1LD_0LE---_1RF1LC_1LE0RA'
def fmt(out): return ' '.join(w if c==1 else '(%s)^%d'%(w,c) for w,c in out)
def rep(S,out):
    # Bell start: biggest run of '1' starts within first 6 cells
    pos=0; best=None
    for i,(w,c) in enumerate(out):
        L=len(w)*c
        if set(w)=={'1'} and (best is None or L>best[1]): best=(pos,L)
        pos+=L
    if best and best[0]<=6: print(S.steps, fmt(out)[:300], flush=True)
t0=time.time()
S=fast.run(M,10**40,9,rep)
print('end',S.steps,S.halted,round(time.time()-t0,1))
