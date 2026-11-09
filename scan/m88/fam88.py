# no. 88 (mirrored): early real phase starts with randomly changed zero runs (parity kept), direct simulation for STEPS steps
import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import random,subprocess,sys,collections,re
from rl import toks_to_rl
M='1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---'.translate(str.maketrans('LR','RL'))
L=[l for l in open('ph88.txt') if l.startswith('PH')][:9]
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2]); STEPS=sys.argv[3]; c=collections.Counter(); ex=[]
for t in range(T):
    l=rnd.choice(L); q=l.split()[2]; f=l.split('|')
    rl=toks_to_rl(f[1]+' '+f[2]+' '+f[3])
    rl2=[]
    for k,(b,n) in enumerate(rl):
        if b==0 and n>=3 and k>2: n=max(1 if n%2 else 2, n+2*rnd.randrange(-10,30))
        rl2.append((b,n))
    tape=''.join(str(b)*n for b,n in rl2)
    r=subprocess.run(['./bsim',M,q,tape,STEPS,'Z'],capture_output=True,text=True).stdout.split()
    c[r[0]]+=1
    if r[0]=='HALT' and len(ex)<6: ex.append((q,tape[:300],r))
print(c)
for e in ex: print(e)
