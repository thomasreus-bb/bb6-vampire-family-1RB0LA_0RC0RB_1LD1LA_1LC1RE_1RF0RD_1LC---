# exact band map of 1RB---_0RC0RD_1LD1RB_0LE0LC_1RA0LF_1LD1LE (empirical, verified against simulation)
# band start (new left cell, state C): 0 (01)^a [0 01 if sep] (11)^b [1 if e]
TAB={(0,0,0):(-1,1,3,1,0),(0,0,1):(-1,0,3,1,-1),(0,1,0):(0,0,1,0,0),(0,1,1):(-1,1,4,1,-1),
     (1,0,0):(0,0,2,0,0),(1,0,1):(0,0,2,0,-1),(1,1,0):(0,1,3,0,0),(1,1,1):(0,0,3,0,-1),
     (2,0,0):(0,0,1,1,0),(2,0,1):(-1,1,4,0,-1),(2,1,0):(0,0,2,1,0),(2,1,1):(0,0,2,1,-1)}
def step(a,sep,b,e):
    d,bead,da,e2,dy=TAB[(b%3,e,sep)]
    m=2*b//3+d
    if b==0: return None
    L=2*a+1+2*sep
    if L>m:   # right register runs empty first: dome, then parallelogram
        a2=2*m+da; Y2=2*a+3*sep-m+dy; return ('D',bead,m,a2,1,(Y2-e2)//2,e2)
    return None
