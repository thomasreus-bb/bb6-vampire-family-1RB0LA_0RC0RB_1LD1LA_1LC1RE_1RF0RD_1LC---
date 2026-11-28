import sys; sys.path.insert(0,'/tmp/an83')
from sym import *
import symbell
def bell_raw(N, r, segs):
    orig=symbell.bell_cfg
    symbell.bell_cfg=lambda N_,r_,runs: ([ZEROS],'B',norm([('1',N_),('0',Lin(r_))]+segs+[REST]),'L')
    try: return symbell.symbell(N,r,[])
    finally: symbell.bell_cfg=orig
if __name__=='__main__':
    for a in (40,38,36,34):
      for r in (1,3):
        for c0 in (101,103):
            segs=[('1',Lin(a)),('0',Lin(2)),('11111100',L(12,k=1)),('1',Lin(6)),('0',Lin(30)),('1',Lin(6))]
            try:
                M,r2,out=bell_raw(L(c0,n=4),r,segs)
                print(a,r,c0,'->',M,r2,' '.join(w+'^('+str(e)+')' for w,e in out))
            except Exception as e: print(a,r,c0,type(e).__name__,str(e)[:100])

def subst(segs, v, sub):
    out=[]
    for w,e in segs:
        if isinstance(e,Lin) and v in e.v:
            k=e.v[v]; rest=Lin(e.c,{a:b for a,b in e.v.items() if a!=v})
            out.append((w, rest + Lin(k,{v:k}) if sub else rest))
        else: out.append((w,e))
    return out
def bell_split(N, r, segs, depth=0, cond=''):
    try:
        M,r2,out=bell_raw(N,r,segs)
        return [(cond, M, r2, out)]
    except NeedSplit as ns:
        w,e=ns.args[0]; vs=sorted(k for k in e.v if k!='n')
        if not vs or depth>8: return [(cond,'NEEDSPLIT',str(ns),None)]
        v=vs[0]; res=[]
        res+=bell_split(N,r,subst(segs,v,0),depth+1,cond+' %s=%d'%(v,0) if False else cond+' [%s=0]'%v)
        res+=bell_split(N,r,subst(segs,v,1),depth+1,cond+' [%s+1]'%v)
        return res
    except Exception as ex: return [(cond,type(ex).__name__,str(ex)[:80],None)]
