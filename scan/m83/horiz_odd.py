import sys,pickle; sys.path.insert(0,'/tmp/an83')
from halt83c import prob, stepc
confs=pickle.load(open('coinconfs.pkl','rb'))
sel=[]
for r,par,runs in confs:
    R=list(runs[:-2])
    if any(x%2 for x in R[:9]) : sel.append((r,par,tuple(R[:16])))
sel=list(dict.fromkeys(sel))
print('configs with odd runs among first 9:',len(sel),flush=True)
D=int(sys.argv[1]); tot=0; pos=[]
for i,(r,par,R) in enumerate(sel):
    p=prob(r,par,list(R),D)
    if p>0: pos.append((p,r,par,R[:9]))
    if i%50==0: print(i,len(pos),stepc.cache_info().currsize,flush=True)
print('positive',len(pos))
for x in sorted(pos,reverse=True)[:20]: print(x)
