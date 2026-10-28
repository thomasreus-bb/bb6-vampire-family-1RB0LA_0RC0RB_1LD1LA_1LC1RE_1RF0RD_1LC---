import subprocess,collections
def one(m,r):
    o=subprocess.run(["./one14",str(m),str(r)],capture_output=True,text=True).stdout.split()
    return o
def pred(m,r):
    if r==0: return (1,2*m+1)
    if r==2 and not (m&(m+1))==0 or (r==2 and m>1 and (m&(m+1))!=0):
        X=3*m+3
    elif r>=2*m: return (2*m+1,r-2*m)
    else: X=3*m+(r+1)//2
    return (X//2,0) if X%2==0 else ((X-1)//2,2)
res=collections.Counter(); halts=[]
for k in range(1,9):
    m=2**k-1
    for r in range(0,2*m+4):
        o=one(m,r)
        if o[0]=="HALT": halts.append((m,r)); res["HALT"]+=1; continue
        got=(int(o[2]),int(o[3])) if o[3:] and o[4]=="0" else ("odd",o)
        p=pred(m,r)
        res["match" if got==p else "other"]+=1
        if got!=p and r%2==1: print("odd r mismatch",m,r,got,p)
for m in range(2,300):
    for r in (0,2):
        o=one(m,r)
        if o[0]=="HALT": halts.append((m,r)); continue
        got=(int(o[2]),int(o[3])); p=pred(m,r)
        if got!=p: res["mismatch m,r=%d"%r]+=1
print(res); print("HALT configs:",halts[:40])
