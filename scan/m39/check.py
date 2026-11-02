import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import chain39 as c, re
c.USE2=True
lines=[l for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'chain_400.txt')) if l.startswith('stage')]
tails=[]
tail=[8]; 
# rebuild tails by rerunning (cheap)
bad=0; halts=0; evens={}
for stage in range(150):
    big=max(tail); N0=10**(len(str(big))+25)
    res=set(); 
    for P in ('','10'):
        for r in (1,3):
            o=c.bell(P,N0+r,tail)
            if o[0]=='HALT': halts+=1; continue
            res.add(tuple(o[2]))
        for r in (0,2):
            o=c.bell(P,N0+r,tail)
            if o[0]=='HALT': halts+=1; continue
            evens[tuple(o[2])]=evens.get(tuple(o[2]),0)+1
    if len(res)!=1: bad+=1; print('stage',stage,'differs',res)
    nt=list(res.pop()); tail=nt[:-1] if nt and nt[-1]==2 else nt
print('stages checked',stage+1,'inconsistent',bad,'halts',halts)
print('even-N outcomes:',evens)
