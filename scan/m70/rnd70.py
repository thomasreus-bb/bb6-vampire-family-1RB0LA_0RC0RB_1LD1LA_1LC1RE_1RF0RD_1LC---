# random "realistic" level starts of no. 70: stack blocks from the sizes seen in the accelerated run, random gaps; run NL levels
import subprocess,random,collections,sys
random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 3)
B=[2,4,4,4,4,4,4,8,8,8,6,9,11,12,15,21]
cnt=collections.Counter();ex=[]
N=int(sys.argv[2]) if len(sys.argv)>2 else 1500
for it in range(N):
    x=6*random.randint(5,60); m=random.choice([11,23,35,21,17])
    toks=[1,x,m]
    for j in range(random.randint(2,12)): toks+=[random.randint(1,40),random.choice(B)]
    tape=' '.join(map(str,toks))
    o=subprocess.run(['./syn70','0',tape,'300000000','4'],capture_output=True,text=True).stdout.strip()
    k=o.split()[0] if 'z0' not in o else 'ok'
    cnt[k]+=1
    if k!='ok': ex.append((tape,o[:50]))
print(cnt); print(ex[:15])
