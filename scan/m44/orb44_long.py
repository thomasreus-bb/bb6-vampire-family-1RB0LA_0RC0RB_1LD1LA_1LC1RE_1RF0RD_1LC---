import os,sys
os.environ['TMCODE']='1RB0RE_1LC0RA_0LD1LB_1LA1LE_0LB0LF_1LD---'
sys.path.insert(0,'.')
from rmodel51 import rules
sys.set_int_max_str_digits(0)
cache={}
def macro(m,r):
    if r not in cache: cache[r]=rules(r)
    for mod,c,l in cache[r]:
        if m%mod==c:
            if l[0] in ('HALT','?'): return l[0],None
            d,mo=l[2]; m0,y0=l[3]
            return l[1], y0+(m-m0)*d//mo
    return '?',None
m,r=15,''; K=int(sys.argv[1]); seq=[]; maxr=0
f=open('/tmp/orb44.txt','w')
for k in range(K):
    seq.append((m%3,r)); maxr=max(maxr,len(r))
    f.write('%d %d %s\n'%(k,m%3,r)); f.flush()
    r2,m2=macro(m,r)
    if r2 in ('HALT','?'): print('stop',r2,'at macro step',k,'r=',r); break
    r,m=r2,m2
print('macro steps',len(seq),'max |r|',maxr,'digits of m',len(str(m)),'distinct r',len(set(x[1] for x in seq)))
t=seq[-1500:]
per=[p for p in range(1,700) if all(t[i]==t[i+p] for i in range(len(t)-p))]
print('eventual period:',per[:3])
