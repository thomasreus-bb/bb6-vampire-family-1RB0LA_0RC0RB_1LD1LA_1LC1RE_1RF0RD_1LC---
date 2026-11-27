import sys
sys.setrecursionlimit(100000)
def drainB(b,w):
    while True:
        if b==0 or b==1: return (w+1,0)
        if b%2==0: m=(b-2)//2; return (5*m+w+6,0)
        if b==3: return (w+1,1)
        if b==5: return None
        q,r=divmod(b-7,6)
        if r==0: return (6*q+w+7,0)
        if r==2: return (5*q+w+6,q+2)
        if r==4: b,w=q,5*q+w+12; continue
def step(k,a,b):
    if a==0: return ('HALT','a0')
    if a==1:
        if b<=1: return ('HALT','a1b%d'%b)
        d=drainB(b-2,5*k+7); return (0,)+d if d else ('HALT','drain')
    if a==2:
        if b==0: return (0,5*k+6,0)
        if b==2: return (0,5*k+6,1)
        if b%2==0: return (k+1,b-3,1)   # b=2m+4 -> a=2m+1
        return (k+1,b+1,0)              # b=2m+1 -> a=2m+2
    if a==3: return (0,5*k+b+6,0)
    if a==5: return (0,5*k+6,b+1)
    if a%2==0:
        n=(a-4)//2; d=drainB(b,2*n+1); return (k+1,)+d if d else ('HALT','drain')
    n=(a-7)//2; return (k+1,2*n+1,b+1)
