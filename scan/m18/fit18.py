import subprocess,collections,fractions,sys
def ev(n,t):
    r=subprocess.run(['./syn18',str(n),t],capture_output=True,text=True).stdout.split()
    return (int(r[0]),r[1],int(r[2])) if r[0]!='HALT' and r[0]!='OVF' else (r[0],None,None)
tails=sys.argv[1:]
for t in tails:
    for mod in (2,4,8,16):
        g=collections.defaultdict(list)
        for n in range(300,300+4*mod):
            m,t2,_=ev(n,t); g[n%mod].append((n,m,t2))
        ok=True; rules=[]
        for r in sorted(g):
            L=g[r]
            if any(type(x[1])!=int for x in L) or len({x[2] for x in L})>1: ok=False;break
            (n1,m1,_),(n2,m2,_)=L[0],L[1]
            a=fractions.Fraction(m2-m1,n2-n1); b=m1-a*n1
            if any(m!=a*n+b for n,m,_ in L): ok=False;break
            rules.append('n≡%d (mod %d): m = %s·n %s %s, tail %s'%(r,mod,a,'+' if b>=0 else '-',abs(b),L[0][2]))
        if ok:
            print('tail',t); [print('  ',x) for x in rules]; break
    else: print('tail',t,': no rule up to mod 16')
