import re
def parse(M):
    T={}
    for i,s in enumerate(M.split("_")):
        for b in range(2):
            x=s[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
    return T
M15="1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC"
M13="1RE0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC"
def F(M,n):
    T=parse(M); tape=bytearray(20*n+400); O=100; 
    for i in range(n): tape[O+i]=1
    tape[O+n+1]=1; tape[O+n+2]=1; p=O+n; q=0; s=0
    while True:
        b=tape[p]
        if s>0 and (q,b)==(0,0):
            nz=[i for i,v in enumerate(tape) if v]; lo,hi=nz[0],nz[-1]; w="".join("01"[tape[i]] for i in range(lo,hi+1))
            m=re.fullmatch(r'(1+)0(11)',w)
            return (len(m.group(1)) if m and p-lo==len(m.group(1)) else ("other",w[:30],p-lo))
        t=T[(q,b)]
        if t is None: return "HALT"
        tape[p]=t[0];p+=t[1];q=t[2];s+=1
        if s>5*10**7: return "TO"
for n in range(4,40):
    print(n, F(M15,n), F(M13,n))
