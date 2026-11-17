# Fast simulator for candidate no. 38 (1RB0RE_1LC0RA_0LD0LB_1RE0LB_1RF---_0RB0RC) on the level of bells.
# State: j (the bell size) and the bell number k inside the current level.
#   next bell in the same level:  j -> (5j + DELTA[k] + [j even]) / 2
#   the level continues after bell k iff j mod 4 is in CONT[k]; otherwise this bell ends the level (X = 0100)
#   level end:  HALT iff j = 20*2^n - 6 or 20*2^n - 5; otherwise the next level starts with j/2 - 3 (j even) or (j-7)/2 (j odd)
# usage:  python3 fast38.py [levels] [print]      e.g.  python3 fast38.py 20000      or   python3 fast38.py 10 print
import sys, collections
DELTA=[1,5,3,3,5,7,3,5,3,5,7,5,3,5,3,5,5,5,5,3,5,3,5,5,5,5,5,3,5,5]
CONT =[(0,1),(0,1),(2,3),(2,3),(2,3),(0,1),(2,3),(2,3),(0,1),(2,3),(0,1),(2,3),(0,1),(2,3),(0,1),(2,3),(0,1),(2,3),(2,3),(0,1),(2,3),(2,3),(2,3),(2,3),(0,1),(2,3),(2,3),(2,3),(2,3),(2,3)]
def is_halt_end(j):
    for c in (6,5):
        x=j+c
        if x%20==0 and (x//20)&(x//20-1)==0: return True
    return False
def main():
    levels=int(sys.argv[1]) if len(sys.argv)>1 else 20000
    show=len(sys.argv)>2
    j,X=121,1                  # level that starts with the bell j = 121 (step 465,865 of the real run)
    hist=collections.Counter(); chance=0.0
    for L in range(levels):
        bells=[j]; k=0
        if X==1:
            while True:
                if k>=len(DELTA): print('level %d has more than %d bells: rules unknown, stop'%(L,len(DELTA))); return
                cont=j%4 in CONT[k]
                j=(5*j+DELTA[k]+(1 if j%2==0 else 0))//2; k+=1; bells.append(j)
                if not cont: break
        hist[len(bells)]+=1; chance+=2/j
        if show: print('level %d: bells %s'%(L,bells))
        if is_halt_end(j): print('HALT at the end of level %d, j = %d'%(L,j)); return
        X=1 if j%4 in (0,1) else 0
        j=j//2-3 if j%2==0 else (j-7)//2
    print('%d levels without HALT; j now has %d digits'%(levels,len(str(j))))
    print('bells per level:',dict(sorted(hist.items())))
    print('sum of the heuristic halting chances 2/j over these levels: %.3e'%chance)
if __name__=='__main__': main()
