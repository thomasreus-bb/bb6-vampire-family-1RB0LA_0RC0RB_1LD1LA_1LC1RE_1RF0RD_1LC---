# no. 73: n units, W = 1^b 0 1^k with b, k up to F*n: halts or leaving the family (00)
import glev2,sys,re
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
g=glev2.G2(M,'D','','110',2,3); form=re.compile(r'1{2,}(01{2,})*')
F=int(sys.argv[2])
for n in range(4,int(sys.argv[1]),3):
    out=[]
    for b in range(2,F*n,1):
        for k in (0,2,3,5):
            W='1'*b+('0'+'1'*k if k else '')
            r,W2=g.pm(n,W,'3000000000')
            if W2 is None: out.append('%s(b%d,k%d)'%(r,b,k))
            elif not (form.fullmatch(W2) or W2==''): out.append('x(b%d,k%d)'%(b,k))
    print(n,len(out),out[:10],flush=True)
