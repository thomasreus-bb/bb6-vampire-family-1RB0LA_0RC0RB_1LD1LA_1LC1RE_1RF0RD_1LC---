# halting chance of no. 70 under small perturbations (as for the vampires): start from the real macro state after L levels,
# change K random gaps among the first 40 stack entries by -3..+3 (gaps stay >= 1), run NL levels with the macro simulator.
import sys,random,pickle,time,os
sys.set_int_max_str_digits(0)
from macro70 import step,RULES,STATS
if os.path.exists('rules70.pkl'): RULES.update(pickle.load(open('rules70.pkl','rb')))
seed,TRIALS,NL,K,T=map(int,sys.argv[1:6]); random.seed(seed)
lev0,x0,S0,_=pickle.load(open('state70.pkl','rb'))
halts=0; levels=0; t0=time.time(); hl=[]
for tr in range(TRIALS):
    S=S0[:]; x=x0
    for k in range(K):
        i=2*random.randint(0,min(40,len(S)//2-1))+1
        S[i]=max(1,S[i]+random.choice([-3,-2,-1,1,2,3]))
    for l in range(NL):
        try: r=step(x,S)
        except Exception as e: print('no rule',e); break
        levels+=1
        if r[0]=='HALT': halts+=1; hl.append(l+1); break
        x,S,_=r
    if time.time()-t0>T: break
print('trials',tr+1,'levels',levels,'HALTs',halts,'at levels',hl[:20],'rules',len(RULES),'%.0f s'%(time.time()-t0))
pickle.dump(dict(RULES),open('rules70.pkl','wb'))
