# invariant test: W = random word without "00" (and not starting with 0); does the next level halt / contain "00"?
import glev2,sys,random,collections
M,st,pre,unit,m,a=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]),int(sys.argv[6])
T=int(sys.argv[7]); NMAX=int(sys.argv[8]); LMAX=int(sys.argv[9]); seed=int(sys.argv[10])
if pre=='-': pre=''
g=glev2.G2(M,st,pre,unit,m,a); rnd=random.Random(seed); c=collections.Counter(); ex=[]
for t in range(T):
    n=rnd.randrange(2,NMAX); L=rnd.randrange(1,LMAX)
    W='1'
    while len(W)<L: W+= '1' if (W[-1]=='0' or rnd.random()<0.7) else '0'
    W=W.rstrip('0')
    r,W2=g.pm(n,W,'3000000000')
    if W2 is None:
        c[r]+=1
        ex.insert(0,(r,n,n%m,W))
    else:
        bad='00' in W2.rstrip('0') or W2.startswith('0')
        c['ok_00' if bad else 'ok']+=1
        if bad and len(ex)<12: ex.append(('00',n,W,W2[:80]))
print(dict(c))
for e in ex: print(e)
