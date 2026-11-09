# no. 73: n units, W = 1^b 0 1^k ; record halts / leaving the family (00) for b in BS, k up to KMAX
import glev2,sys,re
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
g=glev2.G2(M,'D','','110',2,3); form=re.compile(r'1{2,}(01{2,})*')
for n in range(2,int(sys.argv[1])):
    out=[]
    for b in (3,5,8):
        for k in range(2,int(sys.argv[2])):
            r,W2=g.pm(n,'1'*b+'0'+'1'*k,'3000000000')
            if W2 is None: out.append('%s(b%d,k%d)'%(r,b,k))
            elif not (form.fullmatch(W2) or W2==''): out.append('x(b%d,k%d)'%(b,k))
    if out: print(n,out[:12])
