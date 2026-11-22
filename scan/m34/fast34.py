# No. 34 (1RB1RC_1LC1LC_1RE0LD_1LB1RF_---1RA_0RD1RD) uses exactly the event map of no. 50 (m50/fast50.py).
# Renamed (A->D, B->A, C->B, D->E, E->C, F->F) and mirrored, no. 34 is 1RB1RB_1LC0RE_---1LD_1LA1LB_1RA1LF_0LE1LE, started in D:
# it differs from no. 50 only in D0 (1LA instead of 0RA), which matters only for c = 0, never reached.
# Real run: X(1,5) -> X(3,6) -> X(1,15) -> X(13,6) -> ...   Usage: python3 fast34.py [events]
import sys; sys.path.insert(0,__file__.rsplit('/',1)[0]+'/../m50'); from fast50 import step
sys.set_int_max_str_digits(0)
def orbit(a,c,n):
    s_all=s_late=0.0
    for i in range(n):
        m=max(a,c)
        if m<10**300: p=4/max(m,4); s_all+=p; s_late+= p if m>10**5 else 0
        r=step(a,c)
        if r is None: return ('HALT',i,a,c,s_all,s_late)
        a,c=r
    return ('none',n,len(str(max(a,c))),s_all,s_late)
if __name__=='__main__':
    n=int(sys.argv[1]) if len(sys.argv)>1 else 2000000
    print(orbit(1,5,n))
