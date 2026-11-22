# long run of the macro simulator for no. 70; saves the learned rules (rules70.pkl) and a log
import sys,time,pickle,os
import macro70
from macro70 import step,RULES,STATS
sys.set_int_max_str_digits(0)
if os.path.exists('rules70.pkl'): RULES.update(pickle.load(open('rules70.pkl','rb')))
N=int(sys.argv[1]); T=float(sys.argv[2])
x,S,steps=30,[11,18,4],1607; t0=time.time(); small=dict()
for lev in range(1,N+1):
    r=step(x,S)
    if r[0]=='HALT': print('HALT at level',lev,'x digits',len(str(x)),'S',S[:20]); break
    x,S,st=r; steps+=st
    for b in S[2::2]:
        if b<8: small[b]=small.get(b,0)+1
    if lev%2000==0 or time.time()-t0>T:
        print(lev,'levels; steps about 10^%d; x %d digits; stack length %d; rules %d; learned %d; small blocks %s; %.0f s'%(len(str(steps))-1,len(str(x)),len(S),len(RULES),STATS['learned'],sorted(small.items()),time.time()-t0),flush=True)
        if time.time()-t0>T: break
pickle.dump(dict(RULES),open('rules70.pkl','wb'))
pickle.dump((lev,x,S,steps),open('state70.pkl','wb'))
