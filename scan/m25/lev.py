# exact level iteration of no. 25: P(n, W) = 0^inf 1 0 A> 0 1^n W.  For n = 3q + r with q large compared with W, one
# level gives P(4q + e, W') with (e, W') depending only on (r, W).  The table is computed by direct simulation at two
# values of q and checked to agree.
import subprocess,sys,math,pickle,os
def pm(n,W):
    r=subprocess.run(['./pmap','1'*n+W,'40000000000'],capture_output=True,text=True).stdout.split()
    if r[0]!='P': return r[0],None
    s=r[2] if len(r)>2 else ''
    m=len(s)-len(s.lstrip('1'))
    return m,s[m:]
TAB={}
def entry(r,W):
    key=(r,W)
    if key in TAB: return TAB[key]
    res=[]
    for q0 in (len(W)+40, len(W)+47):
        n2,W2=pm(3*q0+r,W)
        if W2 is None: raise RuntimeError('no P from big q: %s'%n2)
        res.append((n2-4*q0,W2))
    if res[0]!=res[1]: raise RuntimeError('not shift invariant %r %r'%(key,res))
    TAB[key]=res[0]; return res[0]
def level(n,W):
    q,r=divmod(n,3)
    if q>=len(W)+40:
        e,W2=entry(r,W); return 4*q+e,W2
    n2,W2=pm(n,W)
    if W2 is None: return n2,None
    return n2,W2
if __name__=='__main__':
    n,W=3,'011'   # first P config: P 47 111011  -> n=3, W='011'
    K=int(sys.argv[1]); maxratio=0; maxlen=0
    for i in range(K):
        n,W=level(n,W)
        if W is None: print('STOP',i,n); break
        ks=[len(x) for x in W.split('0') if x]
        rho=max(ks)/n if ks else 0
        if rho>maxratio: maxratio=rho; print('newmax',i,'log10n=%.1f'%math.log10(n),'W=%s'%('.'.join(map(str,ks))),'k/n=%.3g'%rho,flush=True)
        maxlen=max(maxlen,len(W))
        if i%2000==0: print('lev',i,'log10n=%.1f'%math.log10(n),'W=',('.'.join(map(str,ks))),'tab',len(TAB),flush=True)
    print('done',i+1,'log10n=%.1f'%math.log10(n),'maxlen',maxlen,'tab',len(TAB))
    pickle.dump(TAB,open('tab.pkl','wb'))
