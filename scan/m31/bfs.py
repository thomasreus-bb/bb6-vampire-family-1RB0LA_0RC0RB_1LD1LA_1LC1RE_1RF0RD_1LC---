import sys,json
from fractions import Fraction as Fr
from probe import run
from concurrent.futures import ThreadPoolExecutor
MOD=int(sys.argv[1]) if len(sys.argv)>1 else 6
LIM=int(sys.argv[2]) if len(sys.argv)>2 else 400
def n0_for(P): 
    b=max(3000,20*sum(P)); return b - b%(MOD*9) + MOD*9
table={}
start=[((),0)]
queue=list(start); seen=set(start)
ex=ThreadPoolExecutor(8)
while queue and len(seen)<LIM:
    P,t=queue.pop(0)
    n0=n0_for(P)
    jobs=[]
    for r in range(MOD):
        for k in (0,1):
            n=n0+r+k*MOD*3
            jobs.append((r,k,n,ex.submit(run,P,n,t)))
    ent={}
    for r,k,n,f in jobs:
        res=f.result(); ent.setdefault(r,[]).append((n,res))
    row={}
    for r,lst in ent.items():
        (na,ra),(nb,rb)=lst
        if len(ra)<3 or len(rb)<3:
            row[r]=("SPECIAL",str(ra),str(rb)); continue
        if ra[0]!=rb[0] or ra[2]!=rb[2]: row[r]=("NONCONST",str(ra[:3]),str(rb[:3])); continue
        al=Fr(rb[1]-ra[1],nb-na); be=ra[1]-al*na
        row[r]=(ra[0],ra[2],str(al),str(be))
        key=(ra[0],ra[2])
        if key not in seen: seen.add(key); queue.append(key)
    table[(P,t)]=row
    print(len(table),len(seen),"P=",P,"t=",t, {r:(row[r][0],row[r][1],row[r][2]) if row[r][0] not in("SPECIAL","NONCONST") else row[r] for r in sorted(row)},flush=True)
json.dump({str(k):v for k,v in table.items()},open("table_mod%d.json"%MOD,"w"))
print("closed" if not queue else "open, queue %d"%len(queue))
