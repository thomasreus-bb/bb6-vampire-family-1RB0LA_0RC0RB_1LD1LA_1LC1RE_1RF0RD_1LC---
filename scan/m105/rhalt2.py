# random levels for unit-type machines: n units, W = HEAD (0 1^k)*; which halt within one level?
import glev2,sys,random,collections,re
M,st,pre,unit,m,a,head=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]),int(sys.argv[6]),sys.argv[7]
T=int(sys.argv[8]); NMAX=int(sys.argv[9]); KMAX=int(sys.argv[10]); E=int(sys.argv[11])
if pre=='-': pre=''
g=glev2.G2(M,st,pre,unit,m,a); rnd=random.Random(int(sys.argv[12]) if len(sys.argv)>12 else 1); c=collections.Counter(); ex=[]
for t in range(T):
    n=rnd.randrange(2,NMAX); ks=[rnd.randrange(1,KMAX) for _ in range(rnd.randrange(0,E+1))]
    W=head+''.join('0'+'1'*k for k in ks)
    r,W2=g.pm(n,W,'3000000000')
    if W2 is None:
        c[r]+=1
        if r=='HALT' and len(ex)<25: ex.append((n,n%m,ks))
    else: c['ok' if re.fullmatch(head+r'(01+)*',W2) else 'ok_other']+=1
print(dict(c)); print(ex)
