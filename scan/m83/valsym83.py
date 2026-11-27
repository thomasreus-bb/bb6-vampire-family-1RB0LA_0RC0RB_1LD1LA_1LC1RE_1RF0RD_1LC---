import sys,random,re,subprocess
sys.path.insert(0,'/tmp/an83')
from sym import Lin,L,Halt,Touched,NeedSplit
import symbell
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2])
def inst(e,env): return e.c+sum(x*env[k] for k,x in e.v.items())
ok=bad=skip=0
for it in range(T):
    nb=rnd.randint(1,4); runs=[]; vars_=[]
    for i in range(2*nb-1):
        lo=6 if i%2==0 else 1
        if rnd.random()<0.5:
            runs.append(Lin(rnd.randint(lo,14)))
        else:
            nm='v%d'%i; vars_.append(nm); runs.append(Lin(rnd.randint(lo+7,20),{nm:rnd.choice((2,4))}))
    r=rnd.choice((1,2,3)); c0=rnd.choice((101,103))
    try: M,r2,out=symbell.symbell(L(c0,n=4),r,runs)
    except Halt: res=('HALT',)
    except Exception as e: skip+=1; continue
    else: res=None
    for t in range(2):
        env={k:rnd.randint(0,6) for k in vars_}; env['n']=rnd.randint(0,5)
        N=c0+4*env['n']; cr=[inst(x,env) for x in runs]
        S=''.join(('1' if i%2==0 else '0')*x for i,x in enumerate(cr))+'0'*60+'1'*6
        o=subprocess.run(['./cyc83',str(N),str(r),S,'3000000000'],capture_output=True,text=True).stdout.split()
        if res==('HALT',):
            good = o[0]=='HALT'
        else:
            exp=[inst(e,env) for w,e in out]
            if o[0]!='BELL': good=False
            else:
                rs=[len(x) for x in re.findall(r'0+|1+',o[3])]
                good = int(o[1])==inst(M,env) and int(o[2])==r2 and rs[:len(exp)]==exp
        if good: ok+=1
        else: bad+=1; print('MISMATCH',r,[str(x) for x in runs],env,res or (str(M),r2,[(w,str(e)) for w,e in out]),o[:3])
print('ok',ok,'bad',bad,'skipped (symbolic failed/touched)',skip)
