"""Exact branching search for HALT: from a start (r, N class, S), follow all N residues (both parities as dictated
by the symbolic N') for D Bells using symbell (each step exact for all n in the class)."""
import sys; sys.path.insert(0,'/tmp/an83')
from sym import Lin, L, Halt, Touched, NeedSplit
import symbell
def runs_str(out): return ' '.join(w+str(e) for w,e in out)
def search(r, par, S, D, path, found, prob=1.0):
    if D==0: return
    for c0 in ((101,103) if par else (100,102)):
        try:
            M,r2,out=symbell.symbell(L(c0,n=4),r,[Lin(x) for x in S])
        except Halt:
            found.append((path+[(r,c0,tuple(S[:6]))],prob/2)); continue
        except Exception as e:
            continue
        o=[e.c for w,e in out]
        if len(o)%2==0: o=o[:-1]  # approximate: drop trailing zeros next to the tail sentinel
        pars=(0,1) if any(x%2 for x in M.v.values()) else (M.c%2,)
        for p2 in pars:
            search(r2,p2,o,D-1,path+[(r,c0,tuple(S[:6]))],found,prob/2/len(pars))
if __name__=='__main__':
    tail=[30,6,30,6,30,6]
    for start in ([(2,1,[20,1,6]+tail)], [(3,1,[20,1,6]+tail)], [(1,1,[20,1,6]+tail)], [(1,1,[8,2,12]+tail)]):
        for r,par,S in start:
            found=[]; search(r,par,S,9,[],found)
            print('start',r,par,S[:3],'HALT branches',len(found),'total prob %.3g'%sum(p for _,p in found))
            for f,p in found[:3]: print('   p=%.3g'%p, f)
