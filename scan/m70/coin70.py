# Coin model of no. 70: every rule has the form x' = 3x/2 + c, and the new stack depends only on x mod 12 and a short prefix
# of the stack (checked for all learned rules). In the real run x = 0 mod 6, so only one bit (x/6 even or odd) enters the stack.
# Here this bit is replaced by a fair coin: a fast model of the stack system (no big numbers). It estimates how often a
# random bit sequence leads to HALT, and after how many levels.
# usage: python3 coin70.py seed runs levels_per_run seconds  [start: real|state70]
import sys,random,pickle,os,time,collections
sys.set_int_max_str_digits(0)
import macro70
from macro70 import rule,RULES
if os.path.exists('rules70.pkl'): RULES.update(pickle.load(open('rules70.pkl','rb')))
seed,RUNS,NL,T=map(int,sys.argv[1:5]); random.seed(seed)
start=sys.argv[5] if len(sys.argv)>5 else 'state70'
if start=='real': S0=[11,18,4]
else: S0=pickle.load(open('state70.pkl','rb'))[2]
def merge_front(R):
    pass
def coin_step(S):
    # S = stack as a python list in normal order; use a fake x with the chosen residue
    r=random.choice((0,6)); xf=60+r+12*random.randint(0,3)
    rr=rule(xf,S)
    if rr[0]=='HALT': return None
    _,lp,fits,sf,inf=rr
    vals=[int(a*xf+b) for a,b in fits][1:]
    newp = vals if inf else vals
    if inf: newS=newp
    else: newS=newp+S[lp:]
    # merge zero gaps near the front only (the rest is unchanged)
    i=1; out=[newS[0]]
    lim=len(newp)+2
    while i<len(newS) and i<lim:
        g,b=newS[i],newS[i+1]
        if g==0: out[-1]+=b
        else: out+=[g,b]
        i+=2
    return out+newS[i:]
t0=time.time(); halts=[]; total=0
for run in range(RUNS):
    S=S0[:]
    for l in range(NL):
        S2=coin_step(S); total+=1
        if S2 is None: halts.append(l+1); break
        S=S2
        if time.time()-t0>T: break
    if time.time()-t0>T: break
print('coin model: runs',run+1,'levels',total,'HALTs',len(halts),'at levels',sorted(halts)[:30],'rules',len(RULES),'%.0f s'%(time.time()-t0),flush=True)
pickle.dump(dict(RULES),open(os.environ.get('RULESOUT','rules70.pkl'),'wb'))
