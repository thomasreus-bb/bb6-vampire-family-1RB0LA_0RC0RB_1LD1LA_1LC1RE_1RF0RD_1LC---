import sys,random,re
sys.path.insert(0,'/tmp/an83'); from orb83b import step, rl
from collections import Counter
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2])
def runs(s): return [(m.group(0)[0],len(m.group(0))) for m in re.finditer(r'0+|1+',s)]
def inL2(S,r):
    return r in (1,3) and all(l%2==0 and (l>=6 if c=='1' else l>=2) for c,l in runs(S))
res=Counter(); lens=Counter(); ex=[]
for it in range(T):
    # random L2 word with gap-02 front
    S='1'*(2*rnd.randint(3,25))+'00'
    for i in range(rnd.randint(1,5)):
        S+='1'*(2*rnd.randint(3,20))+'0'*(2*rnd.randint(1,20))
    S+='1'*6+'0'*40+'1'*6
    N=6*rnd.randrange(10**60,10**61)+3; r=rnd.choice((1,3))
    path=[]
    for k in range(30):
        o=step(N,r,S)
        if o[0]!='OK': res[o[0]]+=1; ex.append((o[0],path)); break
        N,r,S=o[1],o[2],o[3]
        path.append((r,' '.join(f'{c}{l}' for c,l in runs(S)[:6])))
        if inL2(S,r): res['back']+=1; lens[k+1]+=1; break
    else: res['stuck']+=1; ex.append(('stuck',path))
print(dict(res), dict(lens))
for e in ex[:6]: print(e)
