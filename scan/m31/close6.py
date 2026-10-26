import json,ast,sys,collections
from fractions import Fraction as Fr
from probe import run
from concurrent.futures import ThreadPoolExecutor
ex=ThreadPoolExecutor(2)
MOD=6
TF="table6.json"
try: T={ast.literal_eval(k):v for k,v in json.load(open(TF)).items()}
except: T={ast.literal_eval(k):v for k,v in json.load(open("table_mod6.json")).items()}
def n0_for(P):
    b=max(3000,20*sum(P)); return b - b%(MOD*9) + MOD*9
def row_for(P,t):
    n0=n0_for(P); jobs=[]
    for r in range(MOD):
        for k in (0,1):
            n=n0+r+k*MOD*3; jobs.append((r,n,ex.submit(run,P,n,t)))
    ent=collections.defaultdict(list)
    for r,n,f in jobs: ent[r].append((n,f.result()))
    row={}
    for r,lst in ent.items():
        (na,ra),(nb,rb)=lst
        if len(ra)<3 or len(rb)<3: row[str(r)]=["SPECIAL",str(ra),str(rb)]; continue
        if ra[0]!=rb[0] or ra[2]!=rb[2]: row[str(r)]=["NONCONST",str(ra[:3]),str(rb[:3])]; continue
        al=Fr(rb[1]-ra[1],nb-na); be=ra[1]-al*na
        row[str(r)]=[list(ra[0]),ra[2],str(al),str(be)]
    return row
M=MOD
while True:
    seen=set(); q=[]
    for x in range(M): seen.add((((),0),x)); q.append((((),0),x))
    missing=set(); halt=[]; bad=[]
    while q:
        s,x=q.pop()
        row=T.get(s)
        if row is None: missing.add(s); continue
        v=row[str(x%6)]
        if v[0]=="SPECIAL":
            halt.append((s,x,v)); continue
        if v[0]=="NONCONST": bad.append((s,x,v)); continue
        s2=(tuple(v[0]),v[1]); al=Fr(v[2]); be=Fr(v[3])
        succ=set()
        if al==1: succ={int(x+be)%M}
        else:
            for t in range(3):
                n2=al*(x+M*t)+be
                if n2.denominator==1: succ.add(int(n2)%M)
        for y in succ:
            if (s2,y) not in seen: seen.add((s2,y)); q.append((s2,y))
    print("pairs",len(seen),"states",len({s for s,x in seen}),"missing",len(missing),"halt",halt[:3],"nonconst",bad[:3],flush=True)
    if not missing: break
    for s in missing:
        T[s]=row_for(*s); print("  computed",s,flush=True)
    json.dump({str(k):v for k,v in T.items()},open(TF,"w"))
json.dump(sorted([ [str(s),x] for s,x in seen]),open("reach6.json","w"))
