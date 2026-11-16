import subprocess,collections,sys,fractions
M=sys.argv[1]; ts=[int(x) for x in sys.argv[2].split(',')]; R=range(int(sys.argv[3]),int(sys.argv[4]))
for t in ts:
    out=collections.defaultdict(list)
    for N in R:
        r=subprocess.run(['./syn',M,str(N),str(t),'200000000'],capture_output=True,text=True).stdout.split()
        out[N].append(r)
    res=[(N,out[N][0]) for N in R]
    halts=[N for N,r in res if r[0]=='HALT']
    other=[(N,r[0]) for N,r in res if r[0] in ('OVF','MAX')]
    ok=[(N,int(r[0]),int(r[1])) for N,r in res if r[0] not in ('HALT','OVF','MAX')]
    # summarise by N mod 6
    g=collections.defaultdict(set)
    for N,a,b in ok: g[N%6].add((a-N, b) if True else None)
    print('t=%d: HALT at N=%s; other %s'%(t,halts[:10],other[:5]))
    for r in sorted(g): print('   N≡%d mod 6: (N\'-N, t\') in %s'%(r,sorted(g[r])[:6]))
