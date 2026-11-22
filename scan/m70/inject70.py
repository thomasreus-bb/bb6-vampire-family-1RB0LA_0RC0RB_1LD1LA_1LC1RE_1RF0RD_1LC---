# injection test for no. 70: in a real macro state, replace the stack block b_j (j = 1..J) by an odd value v,
# run the macro simulator until HALT, until that block is gone (no odd block < 9 left in the first 2J+2 entries) or NL levels.
import sys,random,pickle,time,os,collections
sys.set_int_max_str_digits(0)
from macro70 import step,RULES
if os.path.exists('rules70.pkl'): RULES.update(pickle.load(open('rules70.pkl','rb')))
seed,NL,J,T=map(int,sys.argv[1:5]); vals=list(map(int,sys.argv[5].split(','))); random.seed(seed)
states=pickle.load(open('states70.pkl','rb'))
res=collections.defaultdict(collections.Counter); t0=time.time(); n=0
while time.time()-t0<T:
    lev,x,S=random.choice(states); S=S[:]
    v=random.choice(vals); j=random.randint(1,J); S[2*j]=v
    out='limit'; mn=v
    for l in range(NL):
        try: r=step(x,S)
        except Exception as e: out='norule'; break
        if r[0]=='HALT': out='HALT'; break
        x,S,_=r
        small=[b for b in S[2:2*J+40:2] if b%2 and b<9]
        if small: mn=min(mn,min(small))
        if not small and os.environ.get('EARLY','1')=='1': out='gone'; break
    res[v][out+(' min%d'%mn if mn<v else '')]+=1; n+=1
for v in sorted(res): print('injected',v,dict(res[v]))
pickle.dump(dict(RULES),open('rules70.pkl','wb'))
