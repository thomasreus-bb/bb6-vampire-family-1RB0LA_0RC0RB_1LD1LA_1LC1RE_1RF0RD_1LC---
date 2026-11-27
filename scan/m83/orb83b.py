import sys,subprocess,re,time,pickle
from fractions import Fraction as F
def rl(t): return ' '.join(m.group(0)[0]+str(len(m.group(0))) for m in re.finditer(r'0+|1+',t))
MOD=96
def cyc(n,r,S):
    o=subprocess.run(['/tmp/an83/cyc83',str(n),str(r),S or '-','20000000000'],capture_output=True,text=True).stdout.split()
    return o
def step(N,r,S):
    k=max(2,(4*len(S)+200)//MOD+1); n1=N%MOD+MOD*k
    if N<n1+2*MOD: n1=N
    outs=[cyc(n,r,S) for n in (n1,n1+MOD,n1+2*MOD)]
    if any(o[0]=='HALT' for o in outs): return ('HALT',[o[0] for o in outs])
    if any(o[0]!='BELL' for o in outs): return ('ERR',outs)
    if len({(o[2],o[3]) for o in outs})!=1: return ('ERR-S',[(o[1],o[2],rl(o[3])) for o in outs])
    M=[int(o[1]) for o in outs]
    a=F(M[1]-M[0],MOD); b=M[0]-a*n1
    if M[2]!=a*(n1+2*MOD)+b: return ('ERR-LIN',M)
    Mx=a*N+b; assert Mx.denominator==1
    return ('OK',int(Mx),int(outs[0][2]),outs[0][3],(a,b))
if __name__=='__main__':
    real=pickle.load(open('/tmp/an83/real83.pkl','rb'))
    N,r,S=real[0]; K=int(sys.argv[1]); out=open('/tmp/an83/orb83.txt','w'); t0=time.time(); tl=float(sys.argv[2])
    for k in range(K):
        if k<len(real) and (N,r,S)!=real[k]: out.write("MISMATCH real\n")
        out.write(f"{k} {len(str(N))} {N%96} {r} {rl(S)}\n"); out.flush()
        res=step(N,r,S)
        if res[0]!='OK': out.write(f"STOP {k} {res}\n"); break
        N,r,S=res[1],res[2],res[3]
        if time.time()-t0>tl: break
    out.write(f"done {k} {time.time()-t0:.0f}s\n")
