import json,collections
pairs=json.load(open('onediff.json')); groups=json.load(open('groups607.json'))
info={int(k):v for k,v in json.load(open('info607.json')).items()}
cand={}
for k,l in enumerate(open('../candidates_112.txt').read().split('\n')[1:],1):
    f=l.split()
    if len(f)>=2: cand[f[1]]=k
use={}
for l in open('usage.txt'):
    f=l.split(); j=f.index('|'); c=list(map(int,f[3:j])); la=list(map(int,f[j+1:]))
    use[f[0]]=(int(f[1]),{('ABCDEF'[i//2]+str(i%2)):(c[i],la[i]) for i in range(12)})
tab={}
for n,g in enumerate(groups,1):
    for x in g: tab[x[0]]=n
node=lambda k: ('G%d'%tab[k]) if k in tab else '#%d'%k
def lab(k):
    c=cand.get(info[k][0]); return '#%d%s'%(k,' = [%d](#%d)'%(c,c) if c else '')
def nodelab(v):
    if v[0]=='G':
        g=groups[int(v[1:])-1]; return 'group %s: '%v[1:]+', '.join(lab(x[0]) for x in g)
    return lab(int(v[1:]))
best={}
for k1,s1,v1,k2,s2,v2 in pairs:
    a,b=node(k1),node(k2)
    if a==b: continue
    if a>b: a,b,k1,s1,v1,k2,s2,v2=b,a,k2,s2,v2,k1,s1,v1
    e=(a,b)
    if e not in best or (k1,k2)<best[e][:1]+best[e][3:4]: best[e]=(k1,s1,v1,k2,s2,v2)
adj=collections.defaultdict(set)
for a,b in best: adj[a].add(b); adj[b].add(a)
seen=set(); comps=[]
for v in sorted(adj):
    if v in seen: continue
    st=[v]; c=[]
    while st:
        x=st.pop()
        if x in seen: continue
        seen.add(x); c.append(x); st+=adj[x]
    comps.append(sorted(c,key=lambda v:(v[0],int(v[1:]))))
comps.sort(key=lambda c:(-len(c),c))
def cat(k,s):
    n,la=use[info[k][0]][1][s]
    if n<=20 and la<10**5: return 'start'
    if n<=10000: return 'rare'
    return 'frequent'
def u(k,s):
    n,la=use[info[k][0]][1][s]
    return '%s×'%format(n,',') if cat(k,s)!='start' else '%d× (last at step %s)'%(n,format(la+1,','))
rows=[]; rare=[]
for fi,c in enumerate(comps,1):
    es=[(e,best[e]) for e in best if e[0] in c]
    first=True
    for (a,b),(k1,s1,v1,k2,s2,v2) in sorted(es,key=lambda x:x[1]):
        c1,c2=cat(k1,s1),cat(k2,s2)
        kind='start' if 'start' in (c1,c2) and 'frequent' not in (c1,c2) and not (c1=='rare' or c2=='rare') else ('**rare**' if c1!='frequent' and c2!='frequent' else ('frequent' if c1==c2=='frequent' else 'mixed'))
        if 'rare' in kind: rare.append(fi)
        rows.append('| %s | %s | %s | `%s` %s → `%s` %s | %s / %s | %s |'%(
            str(fi) if first else '', lab(k1)+((' (group %d)'%tab[k1]) if k1 in tab else ''), lab(k2)+((' (group %d)'%tab[k2]) if k2 in tab else ''),
            s1,v1,s2,v2,u(k1,s1),u(k2,s2),kind))
        first=False
nm=sum((len(groups[int(v[1:])-1]) if v[0]=='G' else 1) for c in comps for v in c)
hdr='''## Tables that differ in one transition, among the 607 holdouts (13 Nov 2026)

All 607 machines were compared again, this time allowing **one** different transition, up to renaming of the states and mirroring (`scan/groups607/onediff.py`). Machines with the same table (previous section) count as one table here.

- **%d pairs of tables in %d families, %d machines.** Family sizes (number of tables): %s.
- Column "transition": the transition in which the two machines differ, in each machine's own naming (e.g. `F0 1LA → C1 0RB` means: F0 = `1LA` in the first machine corresponds to C1 = `0RB` in the second).
- Column "used": how often this transition is used in the first 10⁸ steps from the blank tape, in the first / second machine (`usage.c`).
- Column "kind":
  - **start**: the transition is used only in the first few steps (at most 20 times, last use before step 10⁵). After that both machines run with identical tables; they differ only in what the first steps wrote. Such pairs often reach the same configuration and are then equivalent; this is the easiest kind to check.
  - **rare**: used again and again, but at most 10,000 times in 10⁸ steps, e.g. once per Bell as F0 in the vampire family. Between the uses the machines run the same way. These are the best candidates for a shared analysis.
  - **mixed** / **frequent**: used often in one or both machines; the runs are probably quite different.
- Same table and one transition apart does not mean equivalent; whether the runs meet was not checked here.

| family | machine 1 | machine 2 | transition | used in 10⁸ steps | kind |
|---|---|---|---|---|---|
'''%(len(best),len(comps),nm,', '.join('%d × %d'%(v,k) for k,v in sorted(collections.Counter(len(c) for c in comps).items())))
open('onediff_section.md','w').write(hdr+'\n'.join(rows)+'\n\n')
print(len(rows),'rows; families with rare pairs:',sorted(set(rare)))
print(collections.Counter(r.split('|')[-2].strip() for r in rows))
