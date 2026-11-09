# no. 25 inner family: (110)^a 100 1^b T in state A at the left end; run directly to the next left record in A or D, or HALT
import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import random,subprocess,sys,collections
M='1RB0LE_1LC0RD_0RA1LD_0LC1RA_1LF1LA_---1LA'
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2]); c=collections.Counter(); ex=[]
for t in range(T):
    a=rnd.randrange(0,400); b=rnd.randrange(0,800); tl=''.join('0'+'1'*rnd.randrange(1,80) for _ in range(rnd.randrange(0,4)))
    tape='110'*a+'100'+'1'*b+tl
    r=subprocess.run(['./bsim',M,'A',tape,'400000000','D'],capture_output=True,text=True).stdout.split()
    c[r[0]]+=1
    if r[0]=='HALT' and len(ex)<8: ex.append((a,b,tl,r))
print(c)
for e in ex: print(e)
