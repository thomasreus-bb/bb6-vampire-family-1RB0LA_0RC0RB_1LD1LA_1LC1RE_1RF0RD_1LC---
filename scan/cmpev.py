import sys,collections
def load(f):
    R={}
    for l in open(f):
        x=l.split()
        if len(x)<7: continue
        side,st,w,step,h,e1,e2=x; R.setdefault((side,st,int(w)),(int(step),h,e1,e2))
    return R
A=load(sys.argv[1]); B=load(sys.argv[2])
keys=sorted(set(A)&set(B),key=lambda k:k[2])
same=collections.Counter(); lags=[]
for k in keys:
    a,b=A[k],B[k]
    tag=("interior equal" if a[1]==b[1] else "interior differs")+(", ends equal" if (a[2],a[3])==(b[2],b[3]) else ", ends differ")
    same[tag]+=1; lags.append(b[0]-a[0])
print("events A",len(A),"B",len(B),"matching (side,state,width):",len(keys)); print(same)
if lags: print("step lag B-A: first",lags[:5],"last",lags[-5:])
for k in keys[-5:]: print(k,A[k][2:],B[k][2:])
