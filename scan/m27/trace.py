import sys
M=sys.argv[1]; N=int(sys.argv[2]); t0=int(sys.argv[3]); q0=sys.argv[4] if len(sys.argv)>4 else 'C'
S='ABCDEF';T={}
for i,g in enumerate(M.split('_')):
    for b in (0,1):
        x=g[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,S.index(x[2]))
tape={}; p=0; q=S.index(q0); x=1
for i in range(N): tape[x]=1; x+=1
x+=2
for i in range(t0): tape[x]=1; x+=1
lo=0; hi=x; prev=None; st=0
def runs():
    r=[];x=lo
    while x<=hi:
        v=tape.get(x,0);L=0
        while x<=hi and tape.get(x,0)==v: L+=1;x+=1
        r.append(L if v else -L)
    while r and r[-1]<0: r.pop()
    return r
while True:
    b=tape.get(p,0); tr=T[(q,b)]
    if tr is None: print('HALT',st); break
    w,d,q=tr; tape[p]=w; p+=d; st+=1
    if p>hi: hi=p
    if p<lo:
        lo=p; r=runs(); pos=[v for v in r if v>0]
        key=(len(pos), pos[0] if pos else None)
        if not(prev and key[0]==prev[0] and key[1]==prev[1]-2):
            print(st,S[q],r[:14])
        prev=key
        if S[q]=='C' and len(pos)==2 and r[0]==-1 and r[2]==-2 and st>5: break
