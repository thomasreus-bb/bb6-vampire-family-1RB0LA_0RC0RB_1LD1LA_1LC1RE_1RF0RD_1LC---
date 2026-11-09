# no. 88 (mirrored): fully random tapes of 1-runs (length 1..5) and 0-runs (1..40), random state, 10^7 steps; which halt (after >= 1000 steps)?
import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import random,subprocess,sys,collections
M='1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---'.translate(str.maketrans('LR','RL'))
rnd=random.Random(int(sys.argv[1])); c=collections.Counter(); ex=[]
for t in range(int(sys.argv[2])):
    k=rnd.randrange(2,12)
    tape=''.join('0'*rnd.randrange(1,40)+'1'*rnd.randrange(1,6) for _ in range(k))
    q=rnd.choice('BCDE')
    r=subprocess.run(['./bsim',M,q,tape,'10000000','Z'],capture_output=True,text=True).stdout.split()
    key=r[0] if r[0]!='HALT' else ('HALT' if int(r[1])>=1000 else 'HALT<1000')
    c[key]+=1
    if key=='HALT' and len(ex)<5: ex.append((q,tape,r))
print(dict(c))
for e in ex: print(e)
