# C-event rules of mirrored no. 73: X(m, S) with S = [k1, k2, ...]; find how many elements a rule reads and what it emits
import sys,collections
from xm import xmap,sh
def rule(m,k1,k2,k3=None):
    res=[]
    for sent in ([40,7],[43,10]):
        S=[k1,k2]+([k3] if k3 is not None else [])+sent
        r,S2=xmap(m,S)
        if S2 is None: res.append((str(r)[:5],None)); continue
        if S2[-2:]==sent: res.append((r-m,tuple(S2[:-2])))
        else: res.append((r-m,'DEEP:'+sh(S2)[:50]))
    return res
if __name__=='__main__':
    exec(sys.argv[1])
