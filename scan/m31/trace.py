import sys
M="1RB1RF_1RC0LD_1LB1RA_1RE1LE_0RC0LB_0RB---".split("_")
T={}
for i,s in enumerate(M):
    for b in range(2):
        x=s[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
blocks=list(map(int,sys.argv[1].split(","))); maxst=int(sys.argv[2])
MG=20000; tape=bytearray(4*sum(blocks)+100000+MG); p=MG
for i,b in enumerate(blocks):
    for k in range(b): tape[p]=1; p+=1
    if i<len(blocks)-1: p+=1
hi=p; lo=MG; q=0; st=0; last=None
def runs(lo,hi):
    out=[];i=lo
    while i<=hi and tape[i]==0: i+=1
    while i<=hi:
        j=i
        while j<=hi and tape[j]==tape[i]: j+=1
        out.append((tape[i],j-i)); i=j
    return out
while st<maxst:
    t=T[(q,tape[p])]
    if t is None: print("HALT",st); break
    # clean snapshot: head in state A on a 0 with a 1 right of it or at the end
    if q==0 and tape[p]==0:
        r=runs(lo,hi)
        if all(not(s==0 and c>1) for s,c in r[:-1]) :
            hp=p-MG
            sig=" ".join(("%d"%c if s else ("." if c==1 else "z%d"%c)) for s,c in r)
            if sig!=last: print(st,"head@%d"%hp,sig[:200]); last=sig
    tape[p]=t[0]; p+=t[1]; q=t[2]; st+=1
    if p>hi: hi=p
    if p<lo: lo=p
