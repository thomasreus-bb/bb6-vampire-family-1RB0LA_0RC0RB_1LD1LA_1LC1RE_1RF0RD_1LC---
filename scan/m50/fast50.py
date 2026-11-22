# Fast event map for no. 50 (1RB1RB_1LC0RE_---1LD_0RA1LB_1RA1LF_0LE1LE).
# X(a,c) = state E on the first cell of 00 1^a 0 1^c (blank elsewhere); in the real run a is always odd.
# HALT iff c - a in {-2,-1,0,1} (a odd, a >= 3).
def step(a,c):
    if a%2==0: return (a-3,c+6)
    if c-a in (-2,-1,0,1): return None
    if c%2==0: return (c-a-2,3*a+6) if a<c else (a-c-2,3*c+6)
    return (c-a-1,3*a+3) if a<c else (a-c-3,3*c+6)
if __name__=='__main__':
    a,c=15,78
    for i in range(20): print(a,c); a,c=step(a,c)
