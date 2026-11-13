import json,itertools
g=json.load(open('groups607.json')); info={int(k):v for k,v in json.load(open('info607.json')).items()}
cand={}
for k,l in enumerate(open('../candidates_112.txt').read().split('\n')[1:],1):
    f=l.split()
    if len(f)>=2: cand[f[1]]=k
def parse(t):
    d={}
    for i,gg in enumerate(t.split('_')):
        for b in (0,1):
            x=gg[3*b:3*b+3]; d[('ABCDEF'[i],b)]=None if x[0]=='-' else (x[0],x[1],x[2])
    return d
def mirror(d): return {k:(None if v is None else (v[0],'L' if v[1]=='R' else 'R',v[2])) for k,v in d.items()}
def ren(d,P): return {(P[q],b):(None if v is None else (v[0],v[1],P[v[2]])) for (q,b),v in d.items()}
def relate(Y,X):
    dy=parse(Y); dx=parse(X)
    for mir,dd in ((False,dx),(True,mirror(dx))):
        for p in itertools.permutations('ABCDEF'):
            P=dict(zip('ABCDEF',p))
            if ren(dd,P)==dy: return mir,[k for k,v in P.items() if v=='A'][0]
short={'Some structure seen':'structure','Looks like a lottery':'lottery','Rules known, no proof':'rules known','Rules known, no proof, being worked on':'rules known (wip)',
 'Little known':'little known','Little known, being worked on':'little known (wip)','Reported by others':'reported by others','Cryptid':'**cryptid**',
 'Proof in an open PR':'**open PR**','Proof ready, PR soon':'**proof ready**'}
rows=[]
for n,gr in enumerate(g,1):
    base=gr[0][1]
    mem=[]; cls=[]
    for k,code,_,_ in gr:
        c=cand.get(code); st=short.get(info[k][1],info[k][1])
        if code==base: rel='start A'
        else:
            mir,s=relate(code,base); rel='start %s%s'%(s,', mirrored' if mir else '')
        mem.append('#%d%s: %s, %s'%(k,' = [%d](#%d)'%(c,c) if c else '',rel,st))
        if info[k][2] and info[k][2] not in cls: cls.append(info[k][2])
    rows.append('| %d | `%s` | %s | %s |'%(n,base,'<br>'.join(mem),'; '.join(cls) or '–'))
from collections import Counter
sizes=Counter(len(x) for x in g)
hdr='''## Same table among the 607 holdouts (13 Nov 2026)

All 607 machines of the Holdout Guide (status of 3 Nov 2026) were compared, transition table against transition table, up to renaming of the states and mirroring (L ↔ R) (`scan/groups607.py`). Two machines with the same table are the same machine, started in different states, like nos. 51, 61, 71 and 93.

- **130 groups, 335 of the 607 machines.** Group sizes: %s.
- "start X" means: this machine is the machine in column 2 (the first member of the group) started in state X, possibly mirrored. In bbchallenge normal form each start state gives another code.
- Same table does not mean equivalent. The runs from the different starts are different halting questions, unless they meet; this was checked only for the candidates (see *Related machines among the candidates*).
- A proof for one member (e.g. a closed family of configurations that never halts) often transfers to the others if it covers their starts too. Groups where one member already has a proof or a PR are therefore worth a look for the others.
- Column 3: Holdout Guide number, candidate number (if any), start state, guide status (wip = being worked on). Column 4: the guide's classes of the members.

| group | machine (first member) | members | class |
|---|---|---|---|
'''%(', '.join('%d of size %d'%(v,k) for k,v in sorted(sizes.items())))
open('groups_section.md','w').write(hdr+'\n'.join(rows)+'\n\n')
print(hdr[:300]); print(rows[3]); print(rows[26])
