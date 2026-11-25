# split5.py - checks whether 6-state machines are a 5-state machine M5 with one state split into two copies
# that differ only in the halt transition (any start state, mirroring allowed). Usage: edit M5 and Q, run python3 split5.py
import itertools
M5='1RB0LD_0RC1RA_1RD1RE_1LA0LE_0RA0LC'
Q=['1RB0RE_1LC0RA_0LD1LB_1LA1LF_0LB0RD_0LB---','1RB---_0RC1RA_1RD1RF_1LE0LF_1RB0LD_0RE0LC',
   '1RB1RF_1LC0LF_1RD0LB_0RA1RE_1RD---_0RC0LA','1RB0LD_0RC1RA_1RD1RF_1LA0LE_0RA0LC_0RA---']
def parse(x): return [[None if t[0]=='-' else (int(t[0]),t[1],ord(t[2])-65) for t in (r[:3],r[3:])] for r in x.split('_')]
def fmt(T): return '_'.join(''.join('---' if c is None else '%d%s%s'%(c[0],c[1],chr(65+c[2])) for c in r) for r in T)
def iso(T,U):
    """find renaming (start fixed at 0) and mirror mapping T onto U; return (perm,mirror) or None"""
    n=len(T)
    for mir in (0,1):
        for perm in itertools.permutations(range(n)):
            p=perm
            ok=True
            for i in range(n):
                for b in (0,1):
                    a=T[i][b]; c=U[p[i]][b]
                    if (a is None)!=(c is None): ok=False;break
                    if a is None: continue
                    d=a[1] if not mir else 'LR'[a[1]=='L']
                    if (a[0],d,p[a[2]])!=c: ok=False;break
                if not ok: break
            if ok: return p,mir
    return None
U=parse(M5)
for q in Q:
    T=parse(q); found=False
    for a in range(6):
        for b in range(6):
            if a==b: continue
            # b is the copy of a: transitions equal except exactly one where one of them is halt
            diff=[s for s in (0,1) if T[a][s]!=T[b][s]]
            if len(diff)!=1: continue
            s=diff[0]
            if not (T[a][s] is None or T[b][s] is None): continue
            # merged machine: remove b, redirect ->b to a, use non-halt transition
            keep=[i for i in range(6) if i!=b]; idx={i:k for k,i in enumerate(keep)}; idx[b]=idx[a]
            M=[]
            for i in keep:
                row=[]
                for t in (0,1):
                    c=T[i][t]
                    if i==a and t==s: c=T[a][s] if T[a][s] else T[b][s]
                    row.append(None if c is None else (c[0],c[1],idx[c[2]]))
                M.append(row)
            if 0==b: pass
            r=iso(M,U)
            if r:
                found=True; p,mir=r
                hcopy=a if T[a][s] is None else b; other=b if hcopy==a else a
                into=[(chr(65+i),t) for i in range(6) for t in (0,1) if T[i][t] and T[i][t][2]==hcopy]
                # express in M5 naming
                into5=[ (chr(65+p[idx[ord(x)-65]]),t) for x,t in into]
                print(q,': start = M5 state %s;'%chr(65+p[idx[0]]),'states',chr(65+a),'and',chr(65+b),'are copies;','mirrored' if mir else 'not mirrored',
                      '; merged =',fmt(M),'= M5; halting copy',chr(65+hcopy),'(= M5 state %s) halts on symbol %d'%(chr(65+p[idx[hcopy]]),s),
                      '; it is entered by the M5 transitions',into5)
    if not found: print(q,': no split found')
