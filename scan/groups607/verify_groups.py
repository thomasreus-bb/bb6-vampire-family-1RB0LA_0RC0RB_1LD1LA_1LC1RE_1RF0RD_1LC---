# Independent check of the same-table groups: for every member Y of a group, simulate the first member X
# started in the claimed state (mirrored if claimed) and Y from state A, both from the blank tape, step by step,
# and compare states (via the claimed renaming) and tapes for N steps.
import json,itertools,sys
g=json.load(open('groups607.json')); N=int(sys.argv[1])
S='ABCDEF'
def parse(t):
    d={}
    for i,gg in enumerate(t.split('_')):
        for b in (0,1):
            x=gg[3*b:3*b+3]; d[(S[i],b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,x[2])
    return d
def relate(Y,X):
    dy=parse(Y); dx=parse(X)
    for mir in (1,-1):
        for p in itertools.permutations(S):
            P=dict(zip(S,p))
            ok=all((dy[(P[q],b)] is None)==(v is None) and (v is None or dy[(P[q],b)]==(v[0],v[1]*mir,P[v[2]])) for (q,b),v in dx.items())
            if ok: return mir,P
def run_check(X,Y,mir,P):
    dx=parse(X); dy=parse(Y)
    inv={v:k for k,v in P.items()}
    tx={}; ty={}; px=py=0; qx=inv['A']; qy='A'
    for n in range(N):
        if P[qx]!=qy: return 'state differs at step %d'%n
        bx=tx.get(px,0); by=ty.get(py,0)
        if bx!=by: return 'symbol differs at step %d'%n
        a=dx[(qx,bx)]; b=dy[(qy,by)]
        if a is None or b is None: return 'halt at %d (both)'%n if a is None and b is None else 'halt mismatch'
        tx[px]=a[0]; px+=a[1]; qx=a[2]; ty[py]=b[0]; py+=b[1]; qy=b[2]
        if px*mir!=py: return 'position differs at step %d'%n
    return 'ok'
bad=0; n=0
for gr in g:
    X=gr[0][1]
    for k,Y,_,_ in gr[1:]:
        mir,P=relate(Y,X); r=run_check(X,Y,mir,P); n+=1
        if r!='ok': bad+=1; print(gr[0][0],k,r)
print(n,'members checked over',N,'steps each;',bad,'problems')
