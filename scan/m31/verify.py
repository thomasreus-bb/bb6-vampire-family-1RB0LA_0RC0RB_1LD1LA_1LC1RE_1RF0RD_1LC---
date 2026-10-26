import json,ast,random
from fractions import Fraction as Fr
from probe import run
T={ast.literal_eval(k):v for k,v in json.load(open("table6.json")).items()}
random.seed(1)
bad=0;n_ok=0
states=[s for s in T if sum(s[0])<700]
for s in random.sample(states,min(40,len(states))):
    for trial in range(4):
        n=random.randint(4000,9000)
        v=T[s][str(n%6)]
        r=run(s[0],n,s[1])
        if v[0]=="SPECIAL":
            ok = r[0]==ast.literal_eval(v[1])[0]
        elif v[0]=="NONCONST": continue
        else:
            ok = len(r)>=3 and tuple(r[0])==tuple(v[0]) and r[2]==v[1] and r[1]==Fr(v[2])*n+Fr(v[3])
        n_ok+=ok; bad+=not ok
        if not ok: print("MISMATCH",s,n,v,r)
print("checked",n_ok+bad,"mismatches",bad)
