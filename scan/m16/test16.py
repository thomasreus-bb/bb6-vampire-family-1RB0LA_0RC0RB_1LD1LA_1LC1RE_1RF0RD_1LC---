import random,subprocess,sys
sys.path.insert(0,'.')
from macro16 import step
random.seed(1); bad=0; n=0; mx=0; cases={}
for it in range(3000):
    m=random.choice([-1]*20+list(range(3,60)))
    b=random.randint(1,60)
    a=random.choice([random.randint(1,2*b+3), 1, 2*b-1, 2*b-3, 2*b+1, 2*b, 2*b-2])
    if a<1: continue
    o=subprocess.run(['./step16',str(m),str(a),str(b),'300000000'],capture_output=True,text=True).stdout.split()
    p=step(m,a,b)
    if p!="HALT" and p[0]<0 and p[1]==1: p="HALT"
    if o[0]=='MAX': mx+=1; continue
    n+=1
    got="HALT" if o[0]=="HALT" else (int(o[1]),int(o[2]),int(o[3]))
    if got!=p:
        bad+=1
        if bad<20: print((m,a,b),'sim',got,'macro',p)
print('tested',n,'bad',bad,'max',mx)
