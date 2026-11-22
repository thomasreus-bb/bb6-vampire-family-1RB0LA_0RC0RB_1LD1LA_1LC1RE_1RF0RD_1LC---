# Event rules of no. 53 (1RB1RE_1LC1RE_---1LD_1LE0LB_0RF0LD_1RD1RA) on the short configurations (state E on 0, blank to the left):
# P(a) = (10)^a 1 ;  Q(a,b) = (10)^a 11100 (10)^b 1 ;  R(a,b) = (10)^a 11101100 (10)^b 1
# Returns None for HALT and 'LIST' when the next event has more than two long segments.
def step(c):
    t=c[0]
    if t=='P':
        a=c[1]
        return ('P',(3*a+5)//2) if a%2 else ('R',a//2-1,a-1)
    a,b=c[1],c[2]
    if t=='Q':
        if a%2==0: return ('P',3*a//2+b+3)
        if a==1: return None
        if b%2: return ('Q',(a-3)//2,a+(3*b+5)//2)
        return 'LIST'
    if t=='R':
        if a%2==0: return ('Q',a//2+2,a+b)
        if a==1: return None
        return 'LIST'
