# generic exact level iteration: level config = PREFIX 1^n W (state STATE, head left of everything).
# n = m q + r  ->  a q + e  with (e, W') depending only on (r, W) when q is large; table from direct simulation at two q.
import subprocess,sys,math,pickle,os,collections
class G:
    def __init__(s,M,state,prefix,m,a,qmin=40):
        s.M,s.state,s.prefix,s.m,s.a,s.qmin=M,state,prefix,m,a,qmin; s.TAB={}
    def pm(s,n,W,maxsteps='40000000000'):
        r=subprocess.run(['./gmap',s.M,s.state,s.prefix,s.prefix+'1'*n+W,maxsteps],capture_output=True,text=True).stdout.split()
        if r[0]!='P': return r[0],None
        x=r[2] if len(r)>2 else ''
        k=len(x)-len(x.lstrip('1'))
        return k,x[k:]
    def entry(s,r,W):
        key=(r,W)
        if key in s.TAB: return s.TAB[key]
        res=[]
        for q0 in (len(W)+s.qmin, len(W)+s.qmin+7):
            n2,W2=s.pm(s.m*q0+r,W)
            if W2 is None: raise RuntimeError('no level end from q=%d: %s %r'%(q0,n2,key))
            res.append((n2-s.a*q0,W2))
        if res[0]!=res[1]: raise RuntimeError('not shift invariant %r %r'%(key,res))
        s.TAB[key]=res[0]; return res[0]
    def level(s,n,W):
        q,r=divmod(n,s.m)
        if q>=len(W)+s.qmin:
            e,W2=s.entry(r,W); return s.a*q+e,W2
        return s.pm(n,W)
def tails(W): return [len(x) for x in W.split('0') if x]
def run(g,n,W,K,log=None):
    H=collections.Counter(); R=collections.Counter(); mx=0
    for i in range(K):
        n,W=g.level(n,W)
        if W is None: print('STOP at level',i,n); return None
        ks=tails(W); k=max(ks) if ks else 0; H[k]+=1; R[n%g.m]+=1; mx=max(mx,k)
        if log and i%log==0: print('lev',i,'log10n=%.1f'%math.log10(n),'W=','.'.join(map(str,ks)),'tab',len(g.TAB),flush=True)
    print('levels',K,'log10 n=%.1f'%math.log10(n),'max tail entry',mx,'table',len(g.TAB))
    print('residues',dict(R))
    tot=sum(H.values()); acc=0; out=[]
    for k in sorted(H,reverse=True):
        acc+=H[k]; out.append('k>=%d: %.2g'%(k,acc/tot))
    print('; '.join(out))
    return n,W
