# Fast simulator for no. 38 on the level of bells. State: j and the bell number k inside the level.
DELTA=[1,5,3,3,5,7,3,5,3,5,7,5,3,5,3,5,5,5,5,3,5,3,5,5,5,5,5,3,5,5]
CONT =[(0,1),(0,1),(2,3),(2,3),(2,3),(0,1),(2,3),(2,3),(0,1),(2,3),(0,1),(2,3),(0,1),(2,3),(0,1),(2,3),(0,1),(2,3),(2,3),(0,1),(2,3),(2,3),(2,3),(2,3),(0,1),(2,3),(2,3),(2,3),(2,3),(2,3)]
def is_halt_end(j):            # level end with j: HALT iff j = 20*2^n-6 or 20*2^n-5
    for c in (6,5):
        x=j+c
        if x%20==0 and (x//20)&(x//20-1)==0: return True
    return False
def run(j,levels,verbose=False):
    """j = first bell of a level (X=1100). Returns list of levels (bells)."""
    out=[]
    for L in range(levels):
        bells=[j]; k=0
        while True:
            if k>=len(DELTA): return out,('unknown island',k)
            cont = j%4 in CONT[k]
            j=(5*j+DELTA[k]+(1 if j%2==0 else 0))//2; k+=1; bells.append(j)
            if not cont: break
        # bells[-1] is the level end (X=0100)
        if is_halt_end(j): return out+[bells],('HALT at level end, j=%d'%j,None)
        out.append(bells)
        j = j//2-3 if j%2==0 else (j-7)//2
        # level start: X of the first bell must be 1100 (j_end mod 4 in {0,1}); otherwise the new level starts with 0100 directly
    return out,None
if __name__=='__main__':
    levels,st=run(121,6)
    for b in levels: print(b)
    print(st)
