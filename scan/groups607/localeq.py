# Local detour test for tables that differ in one transition (slot q,s).
# Claim checked: for EVERY tape, from a configuration in state q reading s, the two machines
# (M1 with its table, M2 renamed/mirrored into M1's naming) either reach one common configuration
# (M1 after k1>=1 steps, M2 after k2>=1 steps, k1,k2 <= T) or both halt.
# Outside the slot both tables agree, so this implies: M1 halts from c  <=>  M2 halts from c, for every c
# (an infinite run of one machine is cut into blocks between slot uses; each block is matched by
# a nonempty block of the other machine).  Cells are read lazily; an unread cell is branched on 0/1.
# usage: python3 localeq.py [T] [maxbranch]   (writes localeq.txt)
import json,sys,itertools
sys.path.insert(0,'.')
from meetpairs_lib import parse,align
info={int(k):v for k,v in json.load(open('info607.json')).items()}
T=int(sys.argv[1]) if len(sys.argv)>1 else 3000
MAXB=int(sys.argv[2]) if len(sys.argv)>2 else 24
PAIRS=[(52,216),(265,407),(196,404),(81,520),(123,223),(88,312),(88,449),(312,449),(253,432)]

class Need(Exception):
    def __init__(s,c): s.c=c

def run(tab,q,init,T):
    """simulate from state q, head 0, initial tape = init (dict, partial). Returns list of configs
    (state,pos,frozenset(modified cells)) for k=1..; and outcome: 'halt','T'. Raises Need(cell)."""
    tape={}; pos=0; out=[]
    for k in range(T):
        if pos in tape: s=tape[pos]
        elif pos in init: s=init[pos]
        else: raise Need(pos)
        tr=tab[(q,s)]
        if tr is None: return out,'halt'
        w,d,q=int(tr[0]),tr[1],tr[2]
        tape[pos]=w; pos+=1 if d=='R' else -1
        out.append((q,pos,dict(tape)))
    return out,'T'

def eqcfg(a,b,init):
    if a[0]!=b[0] or a[1]!=b[1]: return False
    ta,tb=a[2],b[2]
    for c in set(ta)|set(tb):
        va=ta.get(c, init.get(c)); vb=tb.get(c, init.get(c))
        if va is None or vb is None: raise Need(c)
        if va!=vb: return False
    return True

def check(t1,t2,q,s):
    stack=[{0:s}]; leaves=0; maxk=0
    while stack:
        init=stack.pop()
        if len(init)>MAXB: return ('FAIL: needs more than %d cells'%MAXB, init)
        try:
            r1,o1=run(t1,q,init,T); r2,o2=run(t2,q,init,T)
            if o1=='halt' and o2=='halt': leaves+=1; continue
            # find meeting: index configs of r2 by (state,pos)
            idx={}
            for j,c in enumerate(r2): idx.setdefault((c[0],c[1]),[]).append(j)
            found=None
            for i,c in enumerate(r1):
                for j in idx.get((c[0],c[1]),[]):
                    if eqcfg(c,r2[j],init): found=(i+1,j+1); break
                if found: break
            if found: leaves+=1; maxk=max(maxk,*found); continue
            return ('FAIL: no common configuration within %d steps (outcomes %s/%s)'%(T,o1,o2), init)
        except Need as e:
            for v in (0,1):
                d=dict(init); d[e.c]=v; stack.append(d)
    return ('OK', leaves, maxk)

out=open('localeq.txt','w')
for k1,k2 in PAIRS:
    X=info[k1][0]; Y=info[k2][0]; Y2,Q2,slot=align(X,Y)
    res=check(parse(X),parse(Y2),slot[0],slot[1])
    if res[0]=='OK': line='#%d #%d slot %s%d: OK, all tapes: %d cases (tape windows), common configuration after at most %d steps'%(k1,k2,slot[0],slot[1],res[1],res[2])
    else:
        w=res[1]; line='#%d #%d slot %s%d: %s; first bad window %s'%(k1,k2,slot[0],slot[1],res[0],''.join(str(w[c]) for c in sorted(w))+' (cells %d..%d)'%(min(w),max(w)))
    print(line,flush=True); out.write(line+'\n')
