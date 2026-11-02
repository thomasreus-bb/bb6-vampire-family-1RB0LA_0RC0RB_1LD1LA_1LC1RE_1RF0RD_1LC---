# regime word of each Bell cycle of no. 41 (macro model, exact from Bell 28 on)
import sys
sys.set_int_max_str_digits(100000)
def cycle(n):
    reg, s = 'Q', (2, n-1, 2); w=[]
    while True:
        if reg == 'P1':
            a,b,c = s; k = min(b, c-1); a,b,c = a+3*k, b-k, c-k
            if b == 0: reg, s = 'P2', (a+3, 0, c-4); w.append('d')     # P1 finished: middle used up
            else: reg, s = 'P3', (a+2, b-1, 2); w.append('X')          # right ones used up in P1
        elif reg == 'P2':
            a,b,c = s; ka = max(0, -(-(a-2)//3)); k = min(ka, c-1); a,b,c = a-3*k, b+2*k, c-k
            if a <= 2:
                if a == 0: reg, s = 'P1', (1, b+1, c-1); w.append('L0')
                elif a == 1: reg, s = 'P1', (1, b+2, c-1); w.append('L1')
                else: return w, (b+3, c-2)
            else: reg, s = 'Q', (a, b+1, 2); w.append('Y')                # right ones used up in P2
        else:
            a,b,c = s; c += 2*b+2
            s = (a-3, 1, c) if reg == 'P3' else (a-2, 0, c); reg = 'P2'
def compress(w):
    s=' '.join(w).replace('d L1','D')
    import re
    s=re.sub(r'(D)( D)+', lambda m: 'D^%d'%(m.group(0).count('D')), s)
    return s
if __name__=='__main__':
    n=28; N=int(sys.argv[1])
    from collections import Counter
    pats=Counter()
    for i in range(N):
        w,(x,y)=cycle(n); n2=x+2*y+1
        c=compress(w); import re
        pat=re.sub(r'D\^\d+','D^k',c); pat=re.sub(r'^D ','D^k ',pat); pats[pat]+=1
        if i<int(sys.argv[2]): print(i+2, n, c, '-> A(%d,%d)'%(x,y), n2)
        n=n2
    print(len(pats),'patterns'); 
    for p,c in pats.most_common(30): print(c,p)
