# invariant test at C-event granularity for mirrored no. 73: X(m,S), all runs of S >= 2 -> next event of the same kind?
import random,sys,collections
from xm import xmap,sh
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2]); c=collections.Counter(); ex=[]
for t in range(T):
    m=rnd.randrange(4,300)
    S=[rnd.choice([2,2,2,2,3,5,8,rnd.randrange(2,60)]) for _ in range(rnd.randrange(0,12))]
    r,S2=xmap(m,S,'3000000000')
    if S2 is None:
        c[str(r)[:6]]+=1
        if len(ex)<12: ex.append((m,m%3,sh(S),r))
    elif min(S2,default=2)<2 or r<4:
        c['run<2 or m<4']+=1
        if len(ex)<12: ex.append((m,m%3,sh(S),r,sh(S2)))
    else: c['ok']+=1
print(dict(c))
for e in ex: print(e)
