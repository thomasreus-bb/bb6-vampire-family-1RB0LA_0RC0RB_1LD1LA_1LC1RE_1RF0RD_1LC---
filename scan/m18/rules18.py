from fractions import Fraction as F
import re
from tails import name
def step(n,t):
    """event map of no. 18: (n, tail) -> (m, tail); tails S, P k, Q k, R j"""
    typ=t[0]; k=int(t[1:]) if len(t)>1 else 0
    if typ=='S':
        return (3*n//2+3,'S') if n%2==0 else ((3*n+1)//2,'P0')
    if typ=='R':
        c=3*(k+(k+1)//2)
        if k%2==0 and n==12*k+21: return ('HALT',None)
        return (3*n//2-c,'S') if n%2==0 else ((3*n-2*c-5)//2,'P0')
    r=n%8; m9=F(9*n,8)
    if typ=='P':
        add={0:3,1:F(15,8),2:F(-1,4),3:F(13,8),4:F(1,2),5:F(27,8),6:F(9,4),7:F(1,8)}[r]
        if k==0 and r==5: add=F(19,8)
        def Q(i): return 'S' if i==-1 else ('Q%d'%i)
        nt={0:Q(k-1) if k>=1 else 'S',1:'Q%d'%k,2:'P%d'%(k+1),3:'P%d'%k,4:'P%d'%(k+1),
            5:(Q(k-2) if k>=1 else 'P0'),6:Q(k-1) if k>=1 else 'S',
            7:('P%d'%(3*k//2+3) if k%2==0 else 'R%d'%((3*k-1)//2))}[r]
        return (int(m9+add),nt)
    if typ=='Q':
        add={0:3,1:F(15,8),2:F(-1,4),3:F(21,8),4:F(3,2),5:F(-5,8),6:F(5,4),7:F(1,8)}[r]
        if k==0 and r==0: add=2
        if k==0: nt={0:'P0',1:'S',2:'P3',3:'S',4:'Q0',5:'P1',6:'P0',7:'P1'}[r]
        elif k==1: nt={0:'S',1:'Q0',2:'R1',3:'Q0',4:'Q1',5:'P2',6:'P1',7:'P2'}[r]
        else: nt={0:'Q%d'%(k-2),1:'Q%d'%(k-1),2:('P%d'%(3*k//2+3) if k%2==0 else 'R%d'%((3*k-1)//2)),3:'Q%d'%(k-1),4:'Q%d'%k,5:'P%d'%(k+1),6:'P%d'%k,7:'P%d'%(k+1)}[r]
        return (int(m9+add),nt)
