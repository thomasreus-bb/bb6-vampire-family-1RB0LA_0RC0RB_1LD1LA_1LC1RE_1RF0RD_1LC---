# halting map: which (n, tail) halt within one level
import glev,sys
M,st,pre,m,a=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
tails=sys.argv[6].split(',') ; K=int(sys.argv[7]); NMAX=int(sys.argv[8])
g=glev.G(M,st,pre,m,a)
for tf in tails:
    print('tail pattern',tf)
    for n in range(1,NMAX+1):
        hs=[]
        for k in range(0,K+1):
            W=tf.replace('K','1'*k)
            r,W2=g.pm(n,W,'2000000000')
            if r=='HALT': hs.append(k)
            elif W2 is None: hs.append('%s:%d'%(r,k))
        if hs: print(' n=%d (n mod %d=%d): %s'%(n,m,n%m,hs[:20]))
