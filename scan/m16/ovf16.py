"""no. 16: from R(a,b) = L (1)^a (01)^b [0] in state C (head right of the tape), run to the next
configuration of the same form; L = 1(10)^7 (the frozen left block of the early run)."""
import re, sys
M='1RB1LF_1RC1RF_0LD1RE_---1LC_0RB1RE_1LA0LE'
T=[[None if st[3*b+2]=='-' else (int(st[3*b]),1 if st[3*b+1]=='R' else -1,ord(st[3*b+2])-65) for b in range(2)] for st in M.split('_')]
L='1'+'10'*7
def nxt(a,b,lim=10**7):
    w=L+'1'*a+'01'*b
    t={i:int(c) for i,c in enumerate(w)}; h=len(w); s=2; n=0; hi=h
    while n<lim:
        c=t.get(h,0); tr=T[s][c]
        if tr is None: return ('HALT',n)
        t[h]=tr[0]; h+=tr[1]; s=tr[2]; n+=1
        if h>hi:
            hi=h
            if s==2:
                lo=min(k for k,v in t.items() if v); z=max(k for k,v in t.items() if v)
                ww=''.join(str(t.get(k,0)) for k in range(lo,z+1))
                if ww.startswith(L):
                    m=re.fullmatch(r'(1*)((?:01)*)',ww[len(L):])
                    if m and m.group(1) and m.group(2): return (len(m.group(1)),len(m.group(2))//2,n)
    return ('MAX',)
if __name__=='__main__':
    for b in (15,16,17,31):
        print('b=%d:'%b, [(a,)+nxt(a,b)[:2] for a in range(1,2*b+4)])
