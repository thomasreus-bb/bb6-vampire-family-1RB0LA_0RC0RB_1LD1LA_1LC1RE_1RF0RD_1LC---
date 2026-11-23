# no. 87: round map from (1100)^n TAIL E>  for random tails made of the pieces seen in the run; look for HALT
import subprocess,random,collections,sys
random.seed(int(sys.argv[1])); N=int(sys.argv[2])
P=['100','1111','11','1100']
res=collections.Counter(); ex=[]
for it in range(N):
    tail=''.join(random.choice(P) for _ in range(random.randint(1,6)))+'1111'
    n=random.randint(1,60)
    o=subprocess.run(['./round87',str(n),tail,'300000000'],capture_output=True,text=True).stdout.split()
    k=o[0] if not o[0].isdigit() else 'round'
    res[k]+=1
    if k=='HALT' and len(ex)<12: ex.append((n,tail,o[1]))
print(res); print(ex)
