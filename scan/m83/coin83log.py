import subprocess,random,re,sys,time
P=600
def runs(s): return [m.group(0) for m in re.finditer(r'0+|1+',s)]
def trunc(S):
    if len(S)<=P: return S,False
    rs=runs(S); out=''
    for x in rs:
        if len(out)+len(x)>P: break
        out+=x
    return out.rstrip('0'),True
def traj(seed,S0,K):
    rnd=random.Random(seed); S=S0; r=rnd.choice((1,3)); deep=0; mins={}
    for k in range(K):
        St,cut=trunc(S)
        N=6*rnd.randint(250,350)+3
        o=subprocess.run(['/tmp/an83/cyc83',str(N),str(r),St,'2000000000'],capture_output=True,text=True).stdout.split()
        if o[0]=='HALT': return ('HALT',k,deep,mins,St[:60],r)
        if o[0]!='BELL': return (o[0],k,deep,mins)
        S2=o[3]
        for x in runs(S2[:200]):
            pass
        if len(runs(S2)[0])<6:
            mins['front']=mins.get('front',0)+1
            mins.setdefault('ex',[]).append((k,r,' '.join(x[0]+str(len(x)) for x in runs(St)[:6]),' '.join(x[0]+str(len(x)) for x in runs(S2)[:6]),N%24))
        if cut and St[-40:]!=S2[-40:]: deep+=1
        S=S2+S[len(St):] if cut else S2
        r=rnd.choice((1,3))
    return ('NOHALT',K,deep,mins)
if __name__=='__main__':
    from multiprocessing import Pool
    seeds=int(sys.argv[1]); K=int(sys.argv[2])
    L=[l.split() for l in open('/tmp/an83/orb83.txt') if l.split()[0].isdigit()]
    S0=''.join(x[0]*int(x[1:]) for x in L[-1][4:])
    t0=time.time()
    with Pool(int(sys.argv[3])) as p:
        res=p.starmap(traj,[(s,S0 if s%2==0 else '1'*6,K) for s in range(seeds)])
    for x in res: print(x)
    print('time',time.time()-t0)
