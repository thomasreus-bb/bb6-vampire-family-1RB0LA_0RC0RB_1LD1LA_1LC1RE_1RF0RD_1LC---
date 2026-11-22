# is the rate of "dangerous" events stationary? count per window of 10,000 levels: levels in which an odd stack block < 13 is
# created or touched near the front (prefix of the rule)
import sys,pickle,os,time
sys.set_int_max_str_digits(0)
from macro70 import rule,step,RULES
if os.path.exists('rules70.pkl'): RULES.update(pickle.load(open('rules70.pkl','rb')))
T=float(sys.argv[1]); x,S=30,[11,18,4]; t0=time.time(); lev=0; w={}
while time.time()-t0<T:
    r=rule(x,S); lp=r[1]
    pre=[b for b in S[:lp][2::2] if b%2 and b<13]
    x2,S2,_=step(x,S); nnew=len(S2)-(len(S)-lp)
    post=[b for b in S2[:nnew][2::2] if b%2 and b<13]
    k=lev//10000
    if pre or post: w[k]=w.get(k,0)+1
    x,S=x2,S2; lev+=1
print(lev,'levels; per 10,000 levels, levels touching odd stack blocks 9 or 11:',[w.get(k,0) for k in range(lev//10000+1)])
