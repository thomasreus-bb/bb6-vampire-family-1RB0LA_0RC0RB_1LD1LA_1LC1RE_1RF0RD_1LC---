# Groups of the 607 BB(6) holdouts (Holdout Guide, 3 Nov 2026) with the same transition table up to renaming
# of the states and mirroring (L <-> R), i.e. the same machine started in different states.
import re,itertools,sys,collections
G=open(sys.argv[1]).read().split('\n')
ent=[]
code_re=re.compile(r'^[01-][RL-][A-F-]{1}[01-][RL-][A-F-](_[01-][RL-][A-F-][01-][RL-][A-F-]){5}$')
for i,l in enumerate(G):
    if re.fullmatch(r'#\d+',l.strip()) and i+1<len(G) and code_re.match(G[i+1].strip()):
        ent.append((int(l.strip()[1:]),G[i+1].strip(),G[i+2].strip(),G[i+4].strip() if i+4<len(G) else ''))
print(len(ent),'machines',file=sys.stderr)
cand={}
for k,l in enumerate(open(sys.argv[2]).read().split('\n')[1:],1):
    f=l.split()
    if len(f)>=2: cand[f[1]]=k
def parse(t):
    d={}
    for i,g in enumerate(t.split('_')):
        for b in (0,1):
            x=g[3*b:3*b+3]; d[(i,b)]=None if x[0]=='-' else (x[0],x[1],ord(x[2])-65)
    return d
def canon(d):
    best=None
    for mir in (0,1):
        for p in itertools.permutations(range(6)):
            e=tuple(('-' if d[(q,b)] is None else d[(q,b)][0]+(('L' if d[(q,b)][1]=='R' else 'R') if mir else d[(q,b)][1])+str(p[d[(q,b)][2]])) for q in sorted(range(6),key=lambda q:p[q]) for b in (0,1))
            if best is None or e<best: best=e
    return best
groups=collections.defaultdict(list)
for k,code,st,cls in ent: groups[canon(parse(code))].append((k,code,st,cls))
out=[g for g in groups.values() if len(g)>1]
out.sort(key=lambda g:min(x[0] for x in g))
import json; json.dump(out,open('groups607.json','w'))
print(len(out),'groups,',sum(len(g) for g in out),'machines')
for g in out: print([ (k,cand.get(c)) for k,c,_,_ in g])
