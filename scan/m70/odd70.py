# how do odd blocks change in the real macro run? count, per level, the odd blocks in the touched prefix before and after
import sys,pickle,os,time,collections
sys.set_int_max_str_digits(0)
import macro70
from macro70 import rule,step,RULES
if os.path.exists('rules70.pkl'): RULES.update(pickle.load(open('rules70.pkl','rb')))
T=float(sys.argv[1])
x,S,steps=30,[11,18,4],1607; t0=time.time(); lev=0
trans=collections.Counter(); minodd=10**9
while time.time()-t0<T:
    r=rule(x,S); lp=r[1]
    old=sorted(b for b in S[:lp][2::2] if b%2)   # odd stack blocks b1, b2, ... in the prefix (m excluded)
    x2,S2,st=step(x,S)
    nnew=len(S2)-(len(S)-lp)
    new=sorted(b for b in S2[:nnew][2::2] if b%2)
    if old!=new: trans[(tuple(old),tuple(new))]+=1
    for b in new: minodd=min(minodd,b)
    x,S=x2,S2; lev+=1
print(lev,'levels; smallest odd block ever:',minodd)
# odd blocks other than m (m = 11+6k) are interesting: list the most common changes
shr=sum(c for (a,b),c in trans.items() if b and (not a or min(b)<min(a)))
print('levels where a smaller odd stack block appears:',shr)
for (a,b),c in trans.most_common(40): print(c,a,'->',b)
