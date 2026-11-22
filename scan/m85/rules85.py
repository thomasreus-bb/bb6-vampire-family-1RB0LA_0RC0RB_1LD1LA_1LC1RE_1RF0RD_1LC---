# Corrected event rules for no. 85 (1RB0RF_0LC1RE_---1LD_1LE0LB_0RF0LD_1RD1RA), Discord notation:
# A(a) = E on 0, then (10)^(a-1) 1 ;  B(a,b) = E on 0, then (10)^a 1100 (10)^(b-1) 1   (blank elsewhere)
def v2(x):
    k=0
    while x%2==0: x//=2; k+=1
    return k,x
def step(c):
    if c[0]=='A':
        a=c[1]
        return ('A',3*a//2+2) if a%2==0 else ('B',(a-3)//2,(a+1)//2)
    a,b=c[1],c[2]
    if a%2==0:
        return ('A',3*(a+b)//2+3) if b%2==0 else ('B',(a+b+3)//2,(a+b-1)//2)
    if a%4==3: return ('B',(a+1)//2,b+(a+1)//2)
    k,m=v2(a+3)                      # a = 2^k m - 3, k >= 2, m odd
    if m==1: return ('HALT',)
    if k%2==0: return ('A',(4*a+9+2*m)//3+b)
    if b%2==0: return ('A',(7*a+21+9*b+4*m)//6)
    return ('B',(5*a+3*b-4*m)//6+k+2,(a+4*m+3*b)//6-(k+1)//2)
