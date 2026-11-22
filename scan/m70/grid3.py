import subprocess,random,collections
random.seed(2)
def run(tape,mx=5000000):
    return subprocess.run(['./syn70','0',tape,str(mx)],capture_output=True,text=True).stdout.strip()
H=collections.Counter();ex={};n=0
for it in range(6000):
    k=random.randint(0,4)
    toks=[1,random.choice([6*random.randint(1,15),random.randint(3,90)]),random.choice([11,17,23,35,random.randint(1,40)])]
    for j in range(k):
        toks+= [random.randint(1,30), random.choice([4,8,random.randint(1,12)])]
    tape=' '.join(map(str,toks))
    o=run(tape); n+=1
    key=o.split()[0] if not ('z0' in o) else 'level'
    H[key]+=1; ex.setdefault(key,[]).append((tape,o[:60]))
print(n,H)
for k in ex:
    if k!='level': print(k,ex[k][:8])
