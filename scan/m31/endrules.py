# general end rules: for each irregular orbit transition with exactly one big block (>200),
# re-run the macro step with that block replaced by N = 3000..3000+35 and express the result in N
import subprocess, collections
def mstep(h,blocks):
    o=subprocess.run(["./mstep","200000000",str(h)]+list(map(str,blocks)),capture_output=True,text=True).stdout.split()
    if o[0]!="OK": return (o[0],)
    return (int(o[2]),tuple(map(int,o[4:])))
def conv(hh,b):  # snaps2 h -> blocks-to-the-left h
    return hh+1 if 0<=hh<len(b)-1 else (hh if hh==len(b) else (0 if hh==-1 else hh+1))
pats=collections.OrderedDict()
for l in open("../irrL.txt"):
    a,b=l.strip().split("  ->  ")
    ha,*A=a.split(); A=list(map(int,A)); h=conv(int(ha[1:]),A)
    bigs=[i for i,x in enumerate(A) if x>200]
    if len(bigs)!=1: 
        pats.setdefault(("coupled",),[]).append((h,A)); continue
    i=bigs[0]
    key=(h,tuple("N" if j==i else x for j,x in enumerate(A)))
    pats.setdefault(key,[]).append(A[i])
rules={}
for key,vals in pats.items():
    if key==("coupled",): continue
    h,tmpl=key; i=tmpl.index("N")
    row={}
    for r in range(6):
        outs=[]
        for N in (3000+r,3600+r):
            bl=[N if x=="N" else x for x in tmpl]
            res=mstep(h,bl)
            if len(res)==1: outs.append(res); continue
            hh,ob=res
            outs.append((hh,tuple(("N%+d"%(x-N)) if abs(x-N)<200 else (str(x) if x<200 else "?%d"%x) for x in ob)))
        row[r]= outs[0] if outs[0]==outs[1] else ("NONLIN",outs)
    rules[key]=row
for key,row in rules.items():
    h,tmpl=key
    same=len(set(map(str,row.values())))==1
    print("h%d %-22s"%(h," ".join(map(str,tmpl))), "->", ("all N: h%d %s"%(row[0][0]," ".join(row[0][1])) if same and row[0][0] not in("HALT","TIMEOUT") and len(row[0])==2 else {r:row[r] for r in row}))
print("coupled transitions (two big blocks):",len(pats.get(("coupled",),[])))
