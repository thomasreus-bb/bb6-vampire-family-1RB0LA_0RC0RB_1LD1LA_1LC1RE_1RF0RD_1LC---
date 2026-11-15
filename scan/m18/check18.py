import re,subprocess,random
from rules18 import step
from tails import name
real=[l.split() for l in open('events_real.txt') if 'state E' in l]
seq=[(int(x[4].split('^')[1]),name(x[6])) for x in real]
bad=0
for a,b in zip(seq,seq[1:]):
    s=step(*a)
    if s!=b: bad+=1; print('MISMATCH',a,'->',s,'real',b)
print(len(seq),'real events,',len(seq)-1,'transitions,',bad,'mismatches; last',seq[-1])
# random synthetic check of the rules
random.seed(1); bad=0; N=0
for _ in range(300):
    typ=random.choice('SPQR'); k=random.randint(0,12) if typ!='S' else 0
    if typ=='R' and k==0: k=1
    t={'S':'1','P':'0001'+'01'*k,'Q':'11'+'01'*k,'R':'0001'+'01'*k+'00001'}[typ]
    n=random.randint(150,2500)
    r=subprocess.run(['./syn18',str(n),t],capture_output=True,text=True).stdout.split()
    got=('HALT',None) if r[0]=='HALT' else (int(r[0]),name(r[1]))
    exp=step(n,typ+('' if typ=='S' else str(k)))
    N+=1
    if got!=exp: bad+=1; print('synthetic mismatch',n,typ,k,got,exp)
print(N,'random synthetic checks,',bad,'mismatches')
