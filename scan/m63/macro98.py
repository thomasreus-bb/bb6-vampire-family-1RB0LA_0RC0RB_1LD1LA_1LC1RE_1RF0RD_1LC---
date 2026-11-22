# Macro run of no. 98 with the wiki rules (Marco Dos Santos), checked here on 3,072 synthetic starts (checkC.py).
# The a-loop C(a+2,b) -> C(a,b+3) is done in one jump. A "round" ends when c reaches 0 or 1 (reset or HALT).
# variant '63' uses the rules found for no. 63 (renamed), see notes.
import sys
sys.set_int_max_str_digits(0)
def run(a,b,c,d,maxinner=10**7,variant='98'):
    off=4 if variant=='98' else 3
    rounds=0
    while True:
        if c==0 and d==6: b,d=b+3,3
        if a>=2: b+=3*(a//2); a%=2
        if c>=2:
            # inner loop: (a,b,c) -> (a+b+off, 3, c-2) then a-loop; iterate c//2 times
            n=c//2
            if n>maxinner: return ('stopped',rounds,a,b,c,d)
            for _ in range(n):
                x=a+b+off; a=x%2; b=3+3*(x//2)
            c-=2*n; continue
        rounds+=1
        print('round',rounds,'a=',a,'c=',c,'d=',d,'b parity',b%2,'b digits',len(str(b)),flush=True)
        if variant=='98':
            if c==1 and d==6: a,b,c,d=a+b+4,0,3,3; continue
            if c==0:
                if b%2==0: a,b,c,d=a,0,b//2+3,3; continue
                if a==0: return ('HALT',rounds)
                a,b,c,d=6,3,(b-1)//2,3; continue
            if b%2==1: a,b,c,d=a,0,(b-1)//2+3,6; continue
            if a==0: return ('HALT',rounds)
            if b==0: a,b,c,d=6,0,3,3; continue
            a,b,c,d=6,3,(b-2)//2,6; continue
        else: return ('round end (63 rules for c<=1 not fitted)',)
if __name__=='__main__':
    print(run(4,0,0,3))
