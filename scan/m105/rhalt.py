# random (n, tail) with tails (0 1^k)*: which halt within one level?
import glev,sys,random,collections
M,st,pre,m,a=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
T=int(sys.argv[6]); NMAX=int(sys.argv[7]); KMAX=int(sys.argv[8]); E=int(sys.argv[9])
g=glev.G(M,st,pre,m,a); rnd=random.Random(1); c=collections.Counter(); ex=[]
for t in range(T):
    n=rnd.randrange(1,NMAX); ks=[rnd.randrange(1,KMAX) for _ in range(rnd.randrange(0,E+1))]
    W=''.join('0'+'1'*k for k in ks)
    r,W2=g.pm(n,W,'2000000000')
    import re
    key=('ok' if re.fullmatch(r'(01+)*',W2) else 'ok_otherform') if W2 is not None else r
    if key=='ok_otherform' and len(ex)<15: ex.append(('form',n,ks,W2[:60]))
    c[key]+=1
    if key=='HALT' and len(ex)<15: ex.append((n,ks))
print(dict(c)); print(ex)
