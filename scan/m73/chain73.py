# no. 73: levels with long (011) chains in the tail. Start (110)^n W with W = HEAD (0 11)^j REST, follow up to L levels
# (direct simulation) until HALT, until the chain is gone (no run of >= 6 entries "2" left), or L levels
import glev2,sys,collections,re
M=''.join({'L':'R','R':'L'}.get(c,c) for c in '1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC')
g=glev2.G2(M,'D','','110',2,3)
heads=sys.argv[1].split(','); NS=range(int(sys.argv[2]),int(sys.argv[3])); JF=[float(x) for x in sys.argv[4].split(',')]; L=int(sys.argv[5])
c=collections.Counter(); ex=[]
for head in heads:
    for n0 in NS:
        for jf in JF:
            j=max(1,int(jf*n0))
            n,W=n0,'1'*int(head.split('.')[0])+''.join('0'+'1'*int(x) for x in head.split('.')[1:])+'011'*j
            for lv in range(L):
                r,W2=g.pm(n,W,'20000000000')
                if W2 is None:
                    c[r]+=1
                    if r=='HALT': ex.append((head,n0,j,lv,n))
                    break
                n,W=r,W2
                if '011'*6 not in W: c['chain gone']+=1; break
            else: c['L levels']+=1
print(dict(c))
for e in ex[:20]: print('HALT: head',e[0],'n0',e[1],'j',e[2],'after',e[3],'levels at n',e[4])
