import re,sys; sys.path.insert(0,'/tmp/m100'); from col100 import *
TM='1RB1RD_1LC0RD_1RF1RB_1LE0RA_0LB0LE_---0RC'
T={}
for i,g in enumerate(TM.split('_')):
    for b in (0,1):
        x=g[3*b:3*b+3]
        T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
tape={};p=0;q=0;seen=[]
for s in range(30000000):
    if q==2:
        # check pattern: left of p: (10101)^k , head reads 0 at p, then 1 0 1^a 0 1^b 0...
        lo=min(tape) if tape else 0; hi=max(tape) if tape else 0
        L=''.join(str(tape.get(i,0)) for i in range(lo,p)).lstrip('0')
        R=''.join(str(tape.get(i,0)) for i in range(p,hi+1)).rstrip('0')
        m=re.fullmatch(r'((?:10101)*)',L); m2=re.fullmatch(r'010(1*)0(1*)',R) or re.fullmatch(r'010(1*)',R)
        if m and m2:
            k=len(m.group(1))//5; a=len(m2.group(1)); b=len(m2.group(2)) if m2.lastindex==2 else 0
            seen.append((k,a,b))
            if len(seen)>=40: break
    b=tape.get(p,0); t=T[(q,b)]
    if t is None: print('HALT');break
    tape[p]=t[0]; p+=t[1]; q=t[2]
st=(0,2,0); pred=[st]
for i in range(60): st=step(*st); pred.append(st)
print(seen[:40]); print('subseq of pred?', all(x in pred for x in seen))
