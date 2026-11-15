# Which cells outside the backward context decide the detour?  For each side, take all backward chains
# of depth 8 and the first failing tape; print the cells of that tape that are not fixed by the chain.
import json,sys
sys.argv=['x','8','200']
exec(open('localeq2.py').read().split("out=open('localeq2.txt'")[0])
def firstfail(t1,t2,q,init):
    stack=[dict(init)]
    while stack:
        ini=stack.pop()
        if len(ini)>MAXB: return ini
        try:
            r1,o1=run(t1,q,ini,T); r2,o2=run(t2,q,ini,T)
            if o1=='halt' and o2=='halt': continue
            idx={}
            for j,c in enumerate(r2): idx.setdefault((c[0],c[1]),[]).append(j)
            ok=False
            for i,c in enumerate(r1):
                for j in idx.get((c[0],c[1]),[]):
                    a,b=c[2],r2[j][2]
                    if all(val(a,ini,x,False)==val(b,ini,x,False) for x in set(a)|set(b)): ok=True;break
                if ok: break
            if not ok: return ini
        except Need as e:
            for v in (1,0): d=dict(ini); d[e.c]=v; stack.append(d)
    return None
for k1,k2 in PAIRS[:-1]:
    X=info[k1][0]; Y2,Q2,slot=align(X,info[k2][0]); t1,t2=parse(X),parse(Y2)
    for name,tM,tN in ((k1,t1,t2),(k2,t2,t1)):
        todo=[(slot[0],0,{0:slot[1]},{0:slot[1]},0)]; res=set()
        while todo:
            qq,p,V,C,j=todo.pop()
            if j==8:
                f=firstfail(tM,tN,slot[0],C)
                if f: res.add(tuple(sorted((x,f[x]) for x in f if x not in C))[:4])
                continue
            for q0,p0,V0,nc in preds(tM,qq,p,V):
                C0=dict(C); 
                if nc: C0[nc[0]]=nc[1]
                todo.append((q0,p0,V0,C0,j+1))
        print('#%d/#%d run of #%d: failing extra cells (pos,value), head at 0:'%(k1,k2,name), sorted(res)[:6])
