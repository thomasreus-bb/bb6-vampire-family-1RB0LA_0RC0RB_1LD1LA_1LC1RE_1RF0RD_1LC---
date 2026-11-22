# invariant test for no. 70: level start with every block >= 2 (after the leading 1) -> next level start; does a block of length 1 appear?
import subprocess,random,collections,sys
random.seed(int(sys.argv[1])); N=int(sys.argv[2])
c=collections.Counter(); ex=[]
for it in range(N):
    toks=[1,random.randint(3,150),random.randint(2,40)]
    for j in range(random.randint(0,8)): toks+=[random.randint(1,30),random.randint(2,16)]
    tape=' '.join(map(str,toks))
    o=subprocess.run(['./syn70','0',tape,'20000000'],capture_output=True,text=True).stdout.strip()
    if 'z0' not in o: c[o.split()[0]]+=1; continue
    z0=int(o.split('z0=')[1].split(':')[0]); t=list(map(int,o.split(':')[1].split()))
    if 1 in t[2::2]: c['block1']+=1; ex.append((tape,o.split(':')[1][:60]))
    elif z0: c['z0>0']+=1
    else: c['ok']+=1
print(c,ex[:8])
