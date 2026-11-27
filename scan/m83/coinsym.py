import sys,random,re,pickle
sys.path.insert(0,'/tmp/an83')
from sym import Lin,L,Halt,Touched
import symbell
from collections import Counter
def chain(seed,K,P=400):
    rnd=random.Random(seed)
    Lr=[l.split() for l in open('/tmp/an83/orb83.txt') if l.split()[0].isdigit()]
    runs=[int(x[1:]) for x in Lr[-1][4:]]; r=int(Lr[-1][3]); par=1
    st=Counter(); ex=[]
    for k in range(K):
        # truncate runs to ~P cells, ending with a block
        tot=0; cut=[]
        for i,x in enumerate(runs):
            if tot+x>P and i%2==0 and i>0: break
            cut.append(x); tot+=x
        if len(cut)%2==0: cut=cut[:-1]
        rest=runs[len(cut):]
        c0=rnd.choice((101,103) if par else (100,102))
        try: M,r2,out=symbell.symbell(L(c0,n=4),r,[Lin(x) for x in cut])
        except Halt: st['HALT']+=1; ex.append(('HALT',k,r,par,cut[:8])); break
        except Exception as e: st[type(e).__name__]+=1; break
        o=[e.c for w,e in out]
        if len(o)%2==0:  # ends with zeros: merge into first gap of rest
            rest=[rest[0]+o[-1]]+rest[1:] if rest else rest; o=o[:-1]
        runs=o+rest
        par = (M.c%2) if not any(x%2 for x in M.v.values()) else rnd.randrange(2)
        # record features at this Bell (state before next step): r2, par, small/odd stuff in first 12 runs
        feat=(r2,par, tuple(('g%d'%x if i%2 else 'b%d'%x) for i,x in enumerate(runs[:8]) if (i%2 and (x%2 or x<4)) or (i%2==0 and x<6)))
        st[(r2,par)]+=1
        if feat[2]: ex.append((k,feat,runs[:8]))
        r=r2
    return st,ex
if __name__=='__main__':
    from multiprocessing import Pool
    with Pool(2) as p: res=p.starmap(chain,[(s,3000) for s in range(8)])
    st=Counter(); ex=[]
    for a,b in res: st+=a; ex+=b
    print(st)
    c=Counter((e[1][0],e[1][1],e[1][2]) for e in ex if e[0]!='HALT')
    for k,v in c.most_common(40): print(v,k)
    pickle.dump(ex,open('/tmp/an83/coinsym_ex.pkl','wb'))
