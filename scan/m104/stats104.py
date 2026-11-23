"""stats104.py - Bell statistics for candidate 104 (uses fast104 logic).
Per Bell: eat depth (how far below the post-Bell stack length the stack
shrinks before the next Bell, including scan reads), values in the
stack, growth of the stack.  Usage: python3 stats104.py [bells]"""
import sys, collections, time
def main(N):
    V=[0]; C=[1]; L=[1]
    def push(v,c):
        if c<=0: return
        L[0]+=c
        if V and V[-1]==v: C[-1]+=c
        else: V.append(v); C.append(c)
    def pop():
        v=V[-1]; C[-1]-=1
        if C[-1]==0: V.pop(); C.pop()
        L[0]-=1; return v
    def drain(ks,hi,d):
        while True:
            if hi==0: return d+2
            if hi==1: push(d+1,1); push(0,ks[0]); return 1
            j1,j2=ks[hi-1],ks[hi-2]; hi-=2
            if j1==0: d=2*j2+d+6
            else: push(d+1,1); push(0,j1-1); d=2*j2+5
    d=0; bells=0; last=1; low=1; eats=collections.Counter(); steps_per=collections.Counter()
    nst=0; vmax=0; t=time.time()
    while bells<N:
        if d%2 and len(V)>=2 and V[-1]==3 and C[-1]==1 and V[-2]==0 and C[-2]>=4:
            m=(C[-2]-2)//2; C[-2]-=2*m; L[0]-=2*m; d+=6*m; bells+=1
            if bells>1: eats[last-low]+=1; steps_per[nst]+=1
            last=L[0]; low=last; nst=0
            if bells%20000==0:
                vals=[v for v in V if v]
                print('bell',bells,'len',L[0],'runs',len(V),'max value',max(vals),'maxeat',max(eats),'%.0fs'%(time.time()-t)); sys.stdout.flush()
            continue
        nst+=1; ks=[]
        while True:
            if L[0]==0:
                if d%2: print('HALT', bells); return
                if not ks: push(0,d//2+1); d=1
                else: k0=ks.pop(); push(0,d//2); d=drain(ks,len(ks),2*k0+5)
                break
            e=pop(); low=min(low,L[0])
            if d%2: ks.append(d//2); d=e
            else: d=drain(ks,len(ks),d+e+2); break
    print('eat depth distribution', sorted(eats.items()))
    print('macro steps per Bell', sorted(steps_per.items()))
    print('value histogram', sorted(collections.Counter(V).items())[:40])
main(int(sys.argv[1]) if len(sys.argv)>1 else 20000)
