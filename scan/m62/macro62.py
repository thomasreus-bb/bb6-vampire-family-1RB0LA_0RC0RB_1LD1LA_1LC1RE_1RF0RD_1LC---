# exact macro map of no. 62 (conjectured, checked against direct simulation)
# state (c,b,t): tape 1^c 0 (01)^b (11 if t) 0, state C at a right record
def cycle(c,b,t):
    if c>0:
        if t==0: return (c-1,(3*b+1)//2,0) if b%2 else (c-1,3*b//2+1,1)
        else:    return (c-1,(3*b+3)//2,0) if b%2 else (c-1,3*b//2+2,1)
    if b%2: return 'HALT'
    return (3*b+2+2*t,0,0)
