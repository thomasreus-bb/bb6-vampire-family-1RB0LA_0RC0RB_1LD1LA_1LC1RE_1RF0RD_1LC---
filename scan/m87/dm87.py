# no. 87: the high-level map T of the DeepMind cryptids repository (BusyBeaver/BB6/README.md, kernel-verified in Lean),
# written out in Python.  Configurations: ('R1',n) ('R2',n) ('Q',n) ('S4',n) ('S6',n) or 'HALT'.
import sys
sys.set_int_max_str_digits(0)
CJ=[(4,0),(7,5),(16,4),(22,2),(28,1)]
def E0(H,a):
    return {'Q':[('R1',a+4),('S6',a+6),('R2',a+4),('S6',a+8),('R1',a+4),('S6',a+5),('S6',a+3)],
            'S4':[('R2',a+7),('R1',a+9),('R1',a+9),('S4',a+9),('R1',a+11),('Q',a+9),('R1',a+6)],
            'S6':[('S4',a+9),('R1',a+18),('R1',a+10),'HALT',('R2',a+11),('R1',a+14),('R1',a+15)]}[H]
def tau(k,w):
    q,r=divmod(w,5)
    return {3:[('R1',31*q+10),('Q',31*q+16),('R2',31*q+23),'HALT',('R2',31*q+37)],
            4:[('R1',31*q+16),('R2',31*q+15),('R1',31*q+25),('S6',31*q+28),('R2',31*q+41)],
            5:[('R1',31*q+12),('R1',31*q+15),('R2',31*q+26),('Q',31*q+34),('R1',31*q+45)]}[k][r]
def E1(H,a):
    if H=='Q': return ('S6',a+2)
    if H=='S4': return tau(5,(a+1)//2+1)
    return tau(4,(a+1)//2+1)
def E2(H,a):
    if H=='Q': return ('R1',a+9)
    if H=='S4': return ('R1',a+13)
    return tau(3,(a+8)//2)
def Phi(H,a,b,i,maxit=None):
    it=0
    while True:
        if b==0: return E0(H,a)[i]
        if b==1 and i==0: return E1(H,a)
        if b==1 and i==2: return E2(H,a)
        if i==0:
            q,r=divmod((a+3)//2,5); c,j=CJ[r]; a,b,i=31*q+c,b-2,j
        elif i==2: a,b,i=a+5,b-2,3
        else:
            a,b,i={1:(a+6,b-1,0),3:(a+9,b-1,4),4:(a+3,b-1,5),5:(a+4,b-1,6),6:(a+3,b-1,0)}[i]
        it+=1
        if maxit and it>maxit: return ('TOO_LONG',b)
def T(c,maxit=None):
    k,n=c
    if k=='R1': return ('R1',4) if n==0 else (('R1',6) if n==1 else ('R1',n+5))
    if k=='R2':
        if n==0: return ('R1',4)
        q,r=divmod((n-1)//2,5)
        return [('R1',31*q+8),('R2',31*q+11),('Q',31*q+19),('R2',31*q+26),('R1',31*q+44)][r]
    if n==0: return {'Q':('R1',6),'S4':('R1',10),'S6':('R1',9)}[k]
    if k=='S6' and n==1: return ('R2',23)
    if k=='Q': return Phi('Q',2,n-1,3,maxit)
    if k=='S4': return Phi('S4',2,n-1,3,maxit)
    return Phi('S6',2,n-2,3,maxit)
if __name__=='__main__':
    c=('S6',1); step=0
    while True:
        k,n=c
        big=k in('Q','S4','S6') and n>10**7
        print(step,k,n if n<10**30 else '%d digits'%len(str(n)),flush=True)
        if big: print('next step is a scan of about',len(str(n)),'digit length: out of reach'); break
        c=T(c); step+=1
        if c=='HALT': print('HALT'); break
