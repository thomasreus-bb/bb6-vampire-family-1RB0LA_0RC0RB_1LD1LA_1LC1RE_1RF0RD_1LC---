# no. 25: random tapes 1 0 1^N (0 1^k)* in state D, run directly to the next left record in D or HALT
import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import random,subprocess,sys,collections
M='1RB0LE_1LC0RD_0RA1LD_0LC1RA_1LF1LA_---1LA'
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2]); c=collections.Counter(); ex=[]
for t in range(T):
    N=rnd.randrange(10,1500); tl=''.join('0'+'1'*rnd.randrange(1,60) for _ in range(rnd.randrange(0,4)))
    tape='10'+'1'*N+tl
    r=subprocess.run(['./bsim',M,'D',tape,'2000000000','D'],capture_output=True,text=True).stdout.split()
    c[r[0]]+=1
    if r[0]=='HALT' and len(ex)<10: ex.append((N,tl,r))
print(c); print(ex)
