import sys,re
M="1RB---_0RC0RD_1LD1RB_0LE0LC_1RA0LF_1LD1LE".split("_")
T={}
for i,s in enumerate(M):
    for b in range(2):
        x=s[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
def rle(s):
    return " ".join((m.group()[:2]+"^%d"%(len(m.group())//2)) if len(m.group())>=4 else m.group() for m in re.finditer(r'(?:11)+|(?:01)+|.',s))
a,sep,b,e,nb=map(int,sys.argv[1:6])
s="0"+"01"*a+("001" if sep else "")+"11"*b+("1" if e else "")
tape=bytearray(100000);O=50000
for i,c in enumerate(s): tape[O+i]=int(c)
p=O;q=2;lo=O;hi=O+len(s)-1;st=0;k=0
while k<nb:
    t=T[(q,tape[p])]
    if t is None: print("HALT",st);break
    tape[p]=t[0];p+=t[1];q=t[2];st+=1;hi=max(hi,p)
    if p<lo:
        lo=p
        if q==2: k+=1; print(k,st,rle("".join("01"[x] for x in tape[lo:hi+1])))
