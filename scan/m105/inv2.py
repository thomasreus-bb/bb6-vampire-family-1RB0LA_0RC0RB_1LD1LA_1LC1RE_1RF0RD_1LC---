# invariant test: W = 1^a0 (0 1^k)* with all k >= KMIN; next level: halt? output of the same form?
import glev2,sys,random,collections,re
M,st,pre,unit,m,a=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]),int(sys.argv[6])
T=int(sys.argv[7]); NMAX=int(sys.argv[8]); KMAX=int(sys.argv[9]); E=int(sys.argv[10]); KMIN=int(sys.argv[11]); seed=int(sys.argv[12])
if pre=='-': pre=''
g=glev2.G2(M,st,pre,unit,m,a); rnd=random.Random(seed); c=collections.Counter(); ex=[]
form=re.compile(r'1{%d,}(01{%d,})*'%(KMIN,KMIN))
for t in range(T):
    n=rnd.randrange(2,NMAX)
    W='1'*rnd.randrange(KMIN,KMAX)+''.join('0'+'1'*rnd.randrange(KMIN,KMAX) for _ in range(rnd.randrange(0,E+1)))
    r,W2=g.pm(n,W,'3000000000')
    if W2 is None:
        c[r]+=1
        if len(ex)<12: ex.append((r,n,n%m,W))
    else:
        ok=bool(form.fullmatch(W2)) or W2==''
        c['ok' if ok else 'other']+=1
        if not ok and len(ex)<12: ex.append(('other',n,W,W2[:80]))
print(dict(c))
for e in ex: print(e)
