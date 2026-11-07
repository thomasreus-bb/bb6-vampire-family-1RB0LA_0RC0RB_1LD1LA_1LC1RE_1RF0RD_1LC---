import random,subprocess,sys
import numpy as np
sys.path.insert(0,'.')
from macro16 import step
random.seed(2); data={}
for it in range(1500):
    b=random.randint(3,80); a=random.randint(1,2*b+60)
    if a%2: a+=1
    m=random.choice([-1,5,9])
    u,X=a+2,2*b; M=1
    while (2*M-1)*u-X-2<0: M*=2
    if (2*M-1)*u-X-2==0: continue
    o=subprocess.run(['./step16',str(m),str(a),str(b)],capture_output=True,text=True).stdout.split()
    data.setdefault(M,[]).append((u,X,int(o[0])))
for M,v in sorted(data.items()):
    A=np.array([[u*u,u*X,X*X,u,X,1] for u,X,n in v],float); y=np.array([n for u,X,n in v],float)
    c,res,_,_=np.linalg.lstsq(A,y,rcond=None)
    print(M,len(v),np.round(c,4),'maxerr',np.abs(A@c-y).max())
