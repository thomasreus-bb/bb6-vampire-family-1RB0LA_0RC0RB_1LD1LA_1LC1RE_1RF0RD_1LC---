# hypothesis test: no. 70 halts from a level-start tape only if some block of ones has length 1
import subprocess,random,collections,sys
random.seed(int(sys.argv[1])); N=int(sys.argv[2]); minb=int(sys.argv[3])
H=collections.Counter(); ex=[]
for it in range(N):
    toks=[1,random.randint(3,120),random.randint(minb,40)]
    for j in range(random.randint(0,6)): toks+=[random.randint(1,30),random.randint(minb,14)]
    tape=' '.join(map(str,toks))
    o=subprocess.run(['./syn70','0',tape,'5000000'],capture_output=True,text=True).stdout.strip()
    k='level' if 'z0' in o else o.split()[0]; H[k]+=1
    if k=='HALT': ex.append(tape)
print('min block',minb,H,ex[:10])
