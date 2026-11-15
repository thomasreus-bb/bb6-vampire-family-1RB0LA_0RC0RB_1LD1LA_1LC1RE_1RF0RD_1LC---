# Local detour test with backward context.
# For a pair of tables that differ only in slot (q,s): M = machine whose run we follow, N = the other one.
# Claim: every configuration c of M's run (from the blank tape, start A) that is in state q reading s
# satisfies: M (k1>=1 steps) and N (k2>=1 steps) reach one common configuration from c, or both halt.
# Then an infinite run of M gives an infinite run of N (blocks between slot uses), and the same with
# M and N swapped gives the converse; so both machines halt or both run forever from the blank tape.
# Method: go back j steps along M's table (all ways to reach c); this fixes some cells of c.
# For each backward chain, test the forward claim for ALL tapes that agree with the fixed cells
# (unread cells branched lazily). A chain that fails is extended further back, up to depth D.
# Chains that reach the start configuration (state A, blank tape) are checked on the blank tape directly.
# usage: python3 localeq2.py [D] [T]   (writes localeq2.txt)
import json,sys
from meetpairs_lib import parse,align
info={int(k):v for k,v in json.load(open('info607.json')).items()}
D=int(sys.argv[1]) if len(sys.argv)>1 else 30
T=int(sys.argv[2]) if len(sys.argv)>2 else 200
MAXB=30
PAIRS=[(52,216),(265,407),(196,404),(123,223),(88,312),(88,449),(312,449),(253,432),(81,520)]

class Need(Exception):
    def __init__(s,c): s.c=c

def run(tab,q,init,T,blank=False):
    tape={}; pos=0; out=[]
    for k in range(T):
        if pos in tape: s=tape[pos]
        elif pos in init: s=init[pos]
        elif blank: s=0
        else: raise Need(pos)
        tr=tab[(q,s)]
        if tr is None: return out,'halt'
        w,d,q=int(tr[0]),tr[1],tr[2]
        tape[pos]=w; pos+=1 if d=='R' else -1
        out.append((q,pos,dict(tape)))
    return out,'T'

def val(t,init,c,blank):
    if c in t: return t[c]
    if c in init: return init[c]
    if blank: return 0
    raise Need(c)

def forward(t1,t2,q,init,blank=False):
    """True if for all tapes extending init, the two machines meet (or both halt). Returns (ok, maxk, cases)."""
    stack=[dict(init)]; maxk=0; cases=0
    while stack:
        ini=stack.pop()
        if len(ini)>MAXB: return False,0,cases
        try:
            r1,o1=run(t1,q,ini,T,blank); r2,o2=run(t2,q,ini,T,blank)
            if o1=='halt' and o2=='halt': cases+=1; continue
            idx={}
            for j,c in enumerate(r2): idx.setdefault((c[0],c[1]),[]).append(j)
            found=None
            for i,c in enumerate(r1):
                for j in idx.get((c[0],c[1]),[]):
                    a,b=c[2],r2[j][2]
                    if all(val(a,ini,x,blank)==val(b,ini,x,blank) for x in set(a)|set(b)): found=(i+1,j+1); break
                if found: break
            if not found: return False,0,cases
            cases+=1; maxk=max(maxk,*found)
        except Need as e:
            for v in (0,1): d=dict(ini); d[e.c]=v; stack.append(d)
    return True,maxk,cases

def preds(tab,q,pos,V):
    """backward steps of tab into state q at head pos. V: known cell values at the current time.
    yields (q0,pos0,V0,newC): V0 = values one step earlier; newC = time-0 constraint gained."""
    for (q0,b),tr in tab.items():
        if tr is None or tr[2]!=q: continue
        w=int(tr[0]); d=1 if tr[1]=='R' else -1; x=pos-d
        newC=None
        if x in V:
            if V[x]!=w: continue
        else: newC=(x,w)
        V0=dict(V); V0[x]=b
        yield q0,x,V0,newC

def check_side(tM,tN,q,s):
    # chain state: (state, pos, V (values at that time), C (time-0 constraints), depth)
    todo=[(q,0,{0:s},{0:s},0)]; leaves=0; maxk=0; maxdepth=0; startcases=0
    seen=0
    while todo:
        qq,p,V,C,j=todo.pop(); seen+=1
        if seen>200000: return 'FAIL: too many chains'
        ok,k,c=forward(tM,tN,q,C)
        if ok: leaves+=1; maxk=max(maxk,k); maxdepth=max(maxdepth,j); continue
        # could this chain be the start configuration?  (state A, every known cell 0)
        if qq=='A' and all(v==0 for v in V.values()):
            # the real run: blank tape at time -j, so at time 0 the tape is determined: simulate j steps
            okb,kb,_=forward(tM,tN,q,C,blank=True)  # cells not in C are 0 on the blank-start path
            if not okb: return 'FAIL: start chain of depth %d fails'%j
            startcases+=1
        if j>=D: return 'FAIL: depth %d not enough (context %s)'%(D,''.join('%d'%C[x] for x in sorted(C)))
        for q0,p0,V0,nc in preds(tM,qq,p,V):
            C0=dict(C)
            if nc: C0[nc[0]]=nc[1]
            todo.append((q0,p0,V0,C0,j+1))
    return 'OK (%d backward chains, depth <= %d, common configuration after <= %d steps%s)'%(leaves,maxdepth,maxk,
            ', %d start chains'%startcases if startcases else '')

out=open('localeq2.txt','w')
for k1,k2 in PAIRS:
    X=info[k1][0]; Y2,Q2,slot=align(X,info[k2][0]); t1,t2=parse(X),parse(Y2)
    assert Q2=='A'
    r1=check_side(t1,t2,*slot); r2=check_side(t2,t1,*slot)
    line='#%d/#%d slot %s%d: run of #%d: %s; run of #%d: %s'%(k1,k2,slot[0],slot[1],k1,r1,k2,r2)
    print(line,flush=True); out.write(line+'\n')
