# no. 104 (1RB1RE_1LC1LB_1LE0LD_1LE1LC_0RF1RA_---1RA): DeepMind's accelerated map (cryptids repository,
# BusyBeaver/BB6/Accelerations, section 2.5, kernel-verified in Lean), in Python.
# State E(d, R): state E reading 0 at the left end, then 1^(d+1) 0 1^(r1+1) 0 ...   (R = [r1, r2, ...])
def drain(ks,d,R):
    i=0
    while True:
        if i==len(ks): return (d+2,R)
        if i==len(ks)-1: return (1,[0]*ks[i]+[d+1]+R)
        j1,j2=ks[i],ks[i+1]; i+=2
        if j1==0: d=2*j2+d+6
        else: R=[0]*(j1-1)+[d+1]+R; d=2*j2+5
def step(d,R):
    ks=[]; i=0
    while True:
        if i==len(R):
            if d%2: return None                      # HALT
            if not ks: return (1,[0]*(d//2+1))
            return drain(ks[1:],2*ks[0]+5,[0]*(d//2))
        e=R[i]; i+=1
        if d%2: ks.insert(0,d//2); d=e
        else: return drain(ks,d+e+2,R[i:])
