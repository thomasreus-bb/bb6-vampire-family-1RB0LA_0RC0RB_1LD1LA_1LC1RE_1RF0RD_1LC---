# For every pair of tables that differ in one transition: rename/mirror the second machine into the naming of the first,
# then check with meet2 whether the two runs from the blank tape meet in the same configuration.
# usage: python3 meetpairs.py N1 N2  (writes meetpairs.txt)
import json,itertools,subprocess,sys,collections
info={int(k):v for k,v in json.load(open('info607.json')).items()}
pairs=json.load(open('onediff.json')); groups=json.load(open('groups607.json'))
tab={x[0]:n for n,g in enumerate(groups,1) for x in g}
node=lambda k: ('G%d'%tab[k]) if k in tab else '#%d'%k
S='ABCDEF'
def parse(t):
    d={}
    for i,g in enumerate(t.split('_')):
        for b in (0,1):
            x=g[3*b:3*b+3]; d[(S[i],b)]=None if x[0]=='-' else (x[0],x[1],x[2])
    return d
def code(d): return '_'.join(''.join('---' if d[(q,b)] is None else ''.join(d[(q,b)]) for b in (0,1)) for q in S)
def transform(d,P,mir):
    return {(P[q],b):(None if v is None else (v[0],({'L':'R','R':'L'}[v[1]] if mir else v[1]),P[v[2]])) for (q,b),v in d.items()}
def align(X,Y):
    dx=parse(X); dy=parse(Y)
    for mir in (0,1):
        for p in itertools.permutations(S):
            P=dict(zip(S,p)); t=transform(dy,P,mir)
            diff=[k for k in dx if dx[k]!=t[k]]
            if len(diff)==1: return code(t),P['A'],diff[0]
best={}
for k1,s1,v1,k2,s2,v2 in pairs:
    a,b=node(k1),node(k2)
    if a==b: continue
    e=tuple(sorted((a,b)))
    if e not in best or min(k1,k2)<min(best[e][0],best[e][1]): best[e]=(min(k1,k2),max(k1,k2))
N1,N2=sys.argv[1],sys.argv[2]
out=open('meetpairs.txt','w')
for e,(k1,k2) in sorted(best.items(),key=lambda x:x[1]):
    X=info[k1][0]; Y=info[k2][0]; r=align(X,Y)
    if r is None: print('no alignment',k1,k2); continue
    Y2,Q2,slot=r
    res=subprocess.run(['./meet2',X,'A',Y2,Q2,N1,N2],capture_output=True,text=True).stdout.strip().replace('\n',' | ')
    line='#%d #%d slot %s%d: %s'%(k1,k2,slot[0],slot[1],res)
    print(line,flush=True); out.write(line+'\n'); out.flush()
