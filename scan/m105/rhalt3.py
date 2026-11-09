# random levels with fully random tails (random 0/1 words of length <= LMAX after HEAD)
import glev2,sys,random,collections
M,st,pre,unit,m,a,head=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]),int(sys.argv[6]),sys.argv[7]
T=int(sys.argv[8]); NMAX=int(sys.argv[9]); LMAX=int(sys.argv[10]); p1=float(sys.argv[11])
if pre=='-': pre=''
g=glev2.G2(M,st,pre,unit,m,a); rnd=random.Random(2); c=collections.Counter(); ex=[]
for t in range(T):
    n=rnd.randrange(2,NMAX); L=rnd.randrange(0,LMAX)
    W=head+''.join('1' if rnd.random()<p1 else '0' for _ in range(L)); W=W.rstrip('0')
    r,W2=g.pm(n,W,'3000000000')
    if W2 is None:
        c[r]+=1
        if r=='HALT' and len(ex)<12: ex.append((n,n%m,W))
    else: c['ok']+=1
print(dict(c))
for e in ex: print(e)
