import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import random,subprocess,sys,collections
M='1RB0LE_1LC0RD_0RA1LD_0LC1RA_1LF1LA_---1LA'
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2]); c=collections.Counter(); ex=[]
for t in range(T):
    a=rnd.randrange(0,300); b=rnd.randrange(0,600); tl=''.join('0'+'1'*rnd.randrange(1,60) for _ in range(rnd.randrange(0,4)))
    pre=rnd.choice(['100','1100','10100','110100',''])
    tape='110'*a+pre+'1'*b+tl
    q=rnd.choice('ACD'); stop=rnd.choice('AD')
    r=subprocess.run(['./bsim',M,q,tape,'300000000',stop],capture_output=True,text=True).stdout.split()
    c[r[0]]+=1
    if r[0]=='HALT' and int(r[1])<50: c['trivial']+=1
    elif r[0]=='HALT' and len(ex)<8: ex.append((a,pre,b,tl,q,r))
print(c)
for e in ex: print(e)
