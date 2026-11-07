"""no. 16 = 1RB1LF_1RC1RF_0LD1RE_---1LC_0RB1RE_1LA0LE : exact macro rules (conjectured, checked
against direct simulation).  Configuration at a right record in state C:
    P 1^a (01)^b [0]      P = empty (m = -1)  or  P = 1(10)^m  ("L mode")
E(u,X): smallest M = 1,2,4,... with a' = (2M-1)u - X - 2 >= 0;  b' = X + 1 - (M-1)u;
        if a' == 0 the machine continues to (2b'-1, 1)."""
def E(u,X):
    M=1
    while (2*M-1)*u-X-2<0: M*=2
    a2=(2*M-1)*u-X-2; b2=X+1-(M-1)*u
    assert b2>=1,(u,X)
    if a2==0: return (2*b2-1,1)
    return (a2,b2)
def step(m,a,b):
    """returns (m',a',b') or 'HALT'.  (m=0 is excluded: 1(10)^0 1^a = 1^(a+1).)"""
    if m>=0 and a==1: m,a,b=-1,2,b+m
    r=_step(m,a,b)
    if r!='HALT' and r[0]>=0 and r[1]==1:      # 1(10)^m 1 (01)^b  =  11 (01)^(m+b)
        r=(-1,2,r[2]+r[0])
    return r
def _step(m,a,b):
    if a%2==0 or a>=2*b+1:
        return (m,)+E(a+2,2*b)
    d=2*b+1-a
    if m<0:
        if a==1: return 'HALT'
        if d==2: return (-1,4*b+3,1)
        if d==4: return (-1,2,2*b-1)
        return (a+2,)+E(1,d-3)
    else:
        if d==2: return (-1,2*m+4*b+1,1)
        return (-1,)+E(2*m+2*a+6,2*b-3-a)
