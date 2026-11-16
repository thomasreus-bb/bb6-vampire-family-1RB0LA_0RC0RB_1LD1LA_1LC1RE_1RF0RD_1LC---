# take the clean snapshots of the real orbit, replace every block >= S by a random size with the same residue mod M, run the exact machine on
import sys,random,subprocess,collections
S=int(sys.argv[1]); M=int(sys.argv[2]); N=int(sys.argv[3]); GROW=sys.argv[4]; seed=int(sys.argv[5]); KMAX=sys.argv[6] if len(sys.argv)>6 else '100000000'
rnd=random.Random(seed); snaps=[]
for l in open('snaps.txt'):
    a,b=l.split('|'); t=b.split(); h=int(t[-1][1:]); bl=list(map(int,t[:-1])); snaps.append((h+1 if h<len(bl) else h,bl))
# distinct shapes
shapes={}
for h,bl in snaps: shapes.setdefault((len(bl)-h,)+tuple(x if x<S else 'B%d'%(x%M) for x in bl),(h,bl))
print('snapshots',len(snaps),'distinct classes (exact below %d, else mod %d):'%(S,M),len(shapes))
keys=list(shapes); cfgs=[]
for i in range(N):
    c=rnd.choice(keys); r=c[0]; bl=[]
    for t in c[1:]:
        if isinstance(t,int): bl.append(t)
        else:
            res=int(t[1:]); kmin=-(-(S-res)//M); big=rnd.choice([1,2,4,8,20,40])
            bl.append(res+M*rnd.randrange(kmin,kmin+big))
    cfgs.append((len(bl)-r,bl))
out=subprocess.run(['./mb',KMAX,GROW,'3000000000'],input=''.join('%d %s\n'%(h,' '.join(map(str,b))) for h,b in cfgs),capture_output=True,text=True).stdout.split('\n')
st=collections.Counter(o.split()[0] for o in out[:N]); print(dict(st))
H=[(c,o) for c,o in zip(cfgs,out) if o.startswith('HALT')]
H.sort(key=lambda x:sum(x[0][1]))
for (h,bl),o in H[:10]: print('  HALT after %s macro steps: h=%d'%(o.split()[1],h),bl)
