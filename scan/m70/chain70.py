# chain levels of no. 70 from random realistic starts; record block sizes and gap sizes that appear in the stack, look for blocks of length 1
import subprocess,random,collections,sys
random.seed(int(sys.argv[1])); N=int(sys.argv[2]); L=int(sys.argv[3])
B=[2,4,4,4,4,4,4,8,8,8,6,9,11,12,15,21]
bs=collections.Counter(); bad=[]; res=collections.Counter()
for it in range(N):
    toks=[1,6*random.randint(5,30),random.choice([11,23,35,21,17])]
    for j in range(random.randint(2,12)): toks+=[random.randint(1,40),random.choice(B)]
    tape=' '.join(map(str,toks)); start=tape
    for lev in range(L):
        o=subprocess.run(['./syn70','0',tape,'2000000000'],capture_output=True,text=True).stdout.strip()
        if 'z0' not in o: res[o.split()[0]]+=1; bad.append((start,lev,o[:40])); break
        tape=o.split(':')[1].strip(); t=list(map(int,tape.split()))
        blocks=t[2::2]
        for b in blocks: bs[b]+=1
        if 1 in blocks: bad.append((start,lev,'block 1:',tape[:80]))
        if t[1]>20000: break
    else: res['ok']+=1
    if t[1]>20000: res['big']+=1
print(res); print(sorted(bs.items())[:30]); print(bad[:10])
