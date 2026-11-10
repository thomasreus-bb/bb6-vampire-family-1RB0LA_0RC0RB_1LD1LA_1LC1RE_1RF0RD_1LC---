# exact Bell map of no. 13 (mirrored; B-event tape = 1^n), derived from direct simulation of n < 1100:
#   n odd:                       n' = (3n+5)/2
#   n even, n+2 = 2^k m, m odd:  m = 1 -> HALT;  else F = ((2^(k+1)+1) m + 2k - 1)/2,
#                                n' = F, except m = 3 with k even: n' = (3F+3)/2
import sys,math
def step(n):
    if n%2: return (3*n+5)//2
    x=n+2; k=(x & -x).bit_length()-1; m=x>>k
    if m==1: return None
    F=((2**(k+1)+1)*m+2*k-1)//2
    if m==3 and k%2==0: return (3*F+3)//2
    return F
if __name__=='__main__':
    from f13 import f
    bad=0
    for n in range(1,1100):
        r,_=f(n); s=step(n)
        if (r=='HALT' and s is not None) or (r!='HALT' and r!=s): bad+=1; print('diff',n,r,s)
    print('checked n < 1100 against direct simulation, differences:',bad)
    real=[1,4,8,13,22,28,38,45,70,79,121,184,233,352,443,667,1003,1507,2263,3397,5098,5739,8611,12919,19381,29074,32712]
    n=1; ok=True
    for x in real[1:]:
        n=step(n); ok&=(n==x)
    print('real orbit (26 steps, up to 2e9 steps) reproduced:',ok)
