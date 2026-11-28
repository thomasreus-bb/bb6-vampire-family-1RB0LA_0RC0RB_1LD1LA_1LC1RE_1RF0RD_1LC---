"""Gap-1 case analysis: from every gap-1 context seen in the coin model (first 5 runs), follow all branches
(both N residues per Bell, exact) while a gap 1 is present among the first 9 runs; record the smallest block
behind a gap 1, small fronts, and HALT."""
import sys, re, ast; sys.path.insert(0,'/tmp/an83')
from halt83c import stepc
from collections import Counter
ctxs=Counter()
txt=open('/tmp/an83/coinpar_out2.txt').read().split('\n')[0]
for m in re.finditer(r"\('g1ctx', (\d), (\d), (\d+), (\d+), (\d+), (\d+), (\d+)\): (\d+)", txt):
    r,par,a,b,c,d,e,cnt=map(int,m.groups()); ctxs[(r,par,(a,b,c,d,e))]+=cnt
print('contexts',len(ctxs),sum(ctxs.values()))
TAIL=(30,6,30,6,30,6)
stats=Counter(); worst=[]
def has_g1(S): return any(S[i]==1 for i in range(1,min(9,len(S)),2))
def explore(r,par,S,depth,path):
    if depth>14: stats['depth'] +=1; return
    for c0 in ((101,103) if par else (100,102)):
        res=stepc(r,c0,S+(40,6,40,6))
        if res=='HALT': stats['HALT']+=1; worst.append(('HALT',path+[(r,par,S[:7])])); continue
        if res=='ERR': stats['ERR']+=1; continue
        r2,pars,o=res; o=tuple(o[:-4]) if len(o)>4 else tuple(o)
        o=o[:15] if len(o)>15 else o
        if len(o)%2==0: o=o[:-1]
        for i in range(1,min(9,len(o)-1),2):
            if o[i]==1: stats['blk behind g1=%d'%min(o[i+1],7)]+=1
        if o[0]<=5: stats['front=%d (r=%d)'%(o[0],r2)]+=1
        for p2 in pars:
            if has_g1(o): explore(r2,p2,o,depth+1,path+[(r,par,S[:7])])
            else: stats['exit']+=1
for (r,par,ctx),cnt in ctxs.items():
    explore(r,par,ctx+TAIL,0,[])
print(dict(sorted(stats.items())))
for w in worst[:5]: print(w)
