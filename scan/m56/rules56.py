# no. 56 (1RB1LE_1LB1LC_1RD0LE_---0RB_1RF1LA_0RA0RD): accelerated rules of Polygon (wiki), with step counts.
# A(a,b,c,d,...) = 0^inf 1^a 0 1^b D> 1 0 1^c 0 1^d ... 0 1^k 0^inf ; start A(0,2,0) after 7 steps.
def step(t):
    a,b=t[0],t[1]; rest=list(t[2:]) or [0]
    c=rest[0]; R=rest[1:]
    if b%2==0:
        if b>=4:
            k,v=divmod(b,4)
            return (a+k,v,c+3*k,*R), 8*k*k+4*v*k+k
        if b==2: return (a+2,c+1,*R), 3*c+13
        if a%2==0:
            if a>=4: return (1,a-4,c+4,*R), 4*a-6
            if a==2: return (2,c+2,*R), 3*c+17
            return None,'unreachable A(0,0)'
        if a>=5: return (2,a-4,c+4,*R), 4*a
        if a==3: return 'HALT',16
        return (0,c+4,*R), 3*c+15
    if b>=3:
        if a%2==0:
            if a>=2: return (1,a-2,b-2,c+3,*R), b+4*a+2
            if b>=7:
                k=(b-1)//2; return (0,c+6*k-4,*R), 8*k*k+36*k+3*c-65
            if b==5: return (0,c+8,*R), 3*c+39
            return None,'unreachable A(0,3)'
        if a>=3: return (2,a-2,b-2,c+3,*R), b+4*a+8
        return None,'unreachable A(1,odd)'
    return (0,a+c+3,*R), 3*c+11
def tape(t):
    # list of cells and head index
    a,b=t[0],t[1]; s=[1]*a+[0]+[1]*b; h=len(s); s+=[1]
    for x in t[2:]: s+=[0]+[1]*x
    return s,h
