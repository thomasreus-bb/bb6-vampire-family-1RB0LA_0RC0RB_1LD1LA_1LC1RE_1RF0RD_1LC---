# orbit of no. 69 with Racheline's rules (checked on 2,120 synthetic starts by check69.py), A(N,m) = 0^inf <C (10)^(N-6) 1^m
import sys
sys.set_int_max_str_digits(0)
def step(N,m):
    if m==1: N,m=N+1,0
    if m>=3: return (3*(N//2),m-3) if N%2==0 else (3*(N//2)+1,m-2)
    if m==0: return 'TRANSLATED CYCLER' if N%2==0 else (6,6*(N//2)-15)
    if m==2: return 'HALT' if N%2==0 else (6,6*(N//2)-10)
N,m=6,3; rounds=0; k=0
while True:
    if m>10**7: print('round start A(6, m) with m of %d digits: the next round needs about m/2.5 Bell steps, out of reach'%len(str(m))); break
    r=step(N,m); k+=1
    if isinstance(r,str): print(r); break
    if r[0]==6: rounds+=1; print('round %d starts at Bell %d: A(6, %s)'%(rounds,k,r[1] if r[1]<10**12 else '%d digits'%len(str(r[1]))))
    N,m=r
