import sys,time; sys.path.insert(0,'/tmp/m100'); from col100 import step
from collections import Counter
sys.set_int_max_str_digits(0)
import math
def dg(x): return x.bit_length()*0.30103
def fstep(k,a,b):
    if a>=4 and a%2==0 and b==0:
        j=a//2; return (k+j-1,2,0)
    if a>=7 and a%2==1:
        t=(a-7)//6+1; return (k+t,a-6*t,b+t)
    return step(k,a,b)
if __name__=='__main__':
    s=(0,2,0); t0=time.time(); i=0; c=Counter(); resets=[]
    while time.time()-t0<float(sys.argv[1]):
        k,a,b=s
        key=('a=%d'%a if a<8 else ('aE' if a%2==0 else 'aO'), 'b=%d'%b if b<8 else ('bE' if b%2==0 else 'bO'))
        c[key]+=1
        s2=fstep(*s); i+=1
        if s2[0]=='HALT': print('HALT',i,s,s2); break
        if s2[0]==0: resets.append((round(dg(s2[1])),s2[2] if s2[2]<100 else 'big'))
        s=s2
    print('steps',i,'digits',[round(dg(x)) for x in s])
    print(c.most_common(40)); print('resets',len(resets),resets[-20:])
