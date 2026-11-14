# Within each same-table group: do the runs from the different start states meet (same configuration up to translation)?
# All members are written as the first member X started in some state (and mirrored if needed); mirroring does not
# change whether two runs of X meet. usage: python3 meetgroups.py N1 N2  -> meetgroups.txt
import json,itertools,subprocess,sys
g=json.load(open('groups607.json'))
S='ABCDEF'
def parse(t):
    d={}
    for i,gg in enumerate(t.split('_')):
        for b in (0,1):
            x=gg[3*b:3*b+3]; d[(S[i],b)]=None if x[0]=='-' else (x[0],x[1],x[2])
    return d
def start_in_X(Y,X):
    dy=parse(Y); dx=parse(X)
    for mir in (0,1):
        for p in itertools.permutations(S):
            P=dict(zip(S,p))
            t={(P[q],b):(None if v is None else (v[0],({'L':'R','R':'L'}[v[1]] if mir else v[1]),P[v[2]])) for (q,b),v in dx.items()}
            if t==dy: return [k for k,v in P.items() if v=='A'][0]
N1,N2=sys.argv[1],sys.argv[2]
out=open('meetgroups.txt','w')
for n,gr in enumerate(g,1):
    X=gr[0][1]; st=[(k,start_in_X(c,X)) for k,c,_,_ in gr]
    for (k1,s1),(k2,s2) in itertools.combinations(st,2):
        r=subprocess.run(['./meet2',X,s1,X,s2,N1,N2],capture_output=True,text=True).stdout.strip().replace('\n',' | ')
        line='group %d: #%d (start %s) / #%d (start %s): %s'%(n,k1,s1,k2,s2,r)
        out.write(line+'\n'); out.flush()
print('done')
