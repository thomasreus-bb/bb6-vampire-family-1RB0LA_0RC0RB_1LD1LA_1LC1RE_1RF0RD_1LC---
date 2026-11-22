# On-the-fly macro simulator for no. 70 (1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE); also valid for no. 86 started in B.
# Level start: state A on a blank cell, tape 1 0^x 1^m 0^g1 1^b1 ... ; state = (x, S) with S = [m, g1, b1, g2, b2, ..., b_n].
# A rule maps (x mod M, prefix of S) to an affine function of x (every output number, also the step count: quadratic in x).
# Rules are learned when first needed: the level is simulated directly (lev70.c) for 5 small x of the same residue class,
# with only the prefix on the tape; the head must not reach the next block (otherwise a longer prefix is used).
# Fit from 2 (3 for steps) values, check on the others; on failure M is doubled.
import subprocess,sys,pickle,os
from fractions import Fraction as Fr
sys.set_int_max_str_digits(0)
LEV=os.path.join(os.path.dirname(os.path.abspath(__file__)),'lev70')
if not os.path.exists(LEV): subprocess.run(['gcc','-O2','-o',LEV,LEV+'.c'],check=True)
RULES={}; STATS={'learned':0,'sims':0}
def sim(tape,lim,mx=400000000):
    STATS['sims']+=1
    o=subprocess.run([LEV,' '.join(map(str,tape)),str(lim),str(mx)],capture_output=True,text=True).stdout.split()
    if o[0]!='OK': return (o[0],)
    st,maxp,z0,off=map(int,o[1:5]); blocks=list(map(int,o[6:]))
    return ('OK',st,z0,off,blocks)
def affine(xs,ys):
    a=Fr(ys[1]-ys[0],xs[1]-xs[0]); b=ys[0]-a*xs[0]
    return (a,b) if all(a*x+b==y for x,y in zip(xs,ys)) else None
def quad(xs,ys):
    # fit y = a x^2 + b x + c through the first 3, check the rest
    (x0,x1,x2),(y0,y1,y2)=xs[:3],ys[:3]
    a=Fr((y2-y1)*(x1-x0)-(y1-y0)*(x2-x1),(x2-x1)*(x1-x0)*(x2-x0)); b=Fr(y1-y0,x1-x0)-a*(x1+x0); c=y0-a*x0*x0-b*x0
    return (a,b,c) if all(a*x*x+b*x+c==y for x,y in zip(xs,ys)) else None
def learn(x,S,d,M):
    """try a rule for prefix depth d (uses S[:2d+1] plus the gap S[2d+1] if it exists) and modulus M"""
    inf = 2*d+1>=len(S)
    P=S[:2*d+2] if not inf else S[:]
    r=x%M; xs=[]
    k=max(1,(60-r)//M+1)
    xs=[r+M*(k+i) for i in range(5)]
    outs=[]
    for xt in xs:
        lim=-1 if inf else 1+xt+sum(P)
        o=sim([1,xt]+P,lim)
        outs.append(o)
    kinds=set(o[0] for o in outs)
    if kinds=={'HALT'}: return ('HALT',)
    if 'OUT' in kinds: return 'DEEPER'
    if kinds!={'OK'}: return 'MOD'
    if any(o[2]!=0 for o in outs): return 'MOD'
    L=set(len(o[4]) for o in outs)
    if len(L)!=1: return 'MOD'
    n=L.pop()
    # new list relative: output blocks (first is the leading 1), plus new gap before the untouched part
    vecs=[]
    for xt,o in zip(xs,outs):
        st,z0,off,bl=o[1],o[2],o[3],o[4]
        if bl[0]!=1: return 'MOD'
        tail=[] if inf else [ (1+xt+sum(P)) - (off+sum(bl)) ]
        vecs.append(bl[1:]+tail)
    fits=[]
    for j in range(len(vecs[0])):
        f=affine(xs,[v[j] for v in vecs])
        if f is None: return 'MOD'
        fits.append(f)
    sf=quad(xs,[o[1] for o in outs])
    if sf is None: return 'MOD'
    return ('OK',len(P),fits,sf,inf)
def rule(x,S):
    for d in range(0,len(S)//2+1):
        M=12
        while M<=768:
            key=(x%M,M,tuple(S[:2*d+2]) if 2*d+1<len(S) else ('end',)+tuple(S))
            if key in RULES: res=RULES[key]
            else:
                res=learn(x,S,d,M); RULES[key]=res
                if isinstance(res,tuple): STATS['learned']+=1
            if res=='MOD': M*=2; continue
            break
        if res=='DEEPER': continue
        if res=='MOD': raise Exception('no rule found (modulus)')
        return res
    raise Exception('no rule found (depth)')
def step(x,S):
    """one level: returns (x', S', steps) or ('HALT',)"""
    r=rule(x,S)
    if r[0]=='HALT': return ('HALT',)
    _,lp,fits,sf,inf=r
    vals=[a*x+b for a,b in fits]
    assert all(v.denominator==1 and v>=0 for v in vals), (x,S,vals)
    vals=[int(v) for v in vals]
    a,b,c=sf; st=a*x*x+b*x+c; assert st.denominator==1
    newS=vals[1:]+([] if inf else S[lp:]) if not inf else vals[1:]
    if not inf:
        # vals[-1] is the new gap before the untouched part S[lp:], which starts with a block
        newS=vals[1:-1]+[vals[-1]]+S[lp:]
    # merge zero gaps (blocks touching): a 0 gap means two blocks join
    out=[newS[0]]; i=1
    while i<len(newS):
        g,b_=newS[i],newS[i+1]
        if g==0: out[-1]+=b_
        else: out+= [g,b_]
        i+=2
    return (vals[0],out,int(st))
if __name__=='__main__':
    import time
    N=int(sys.argv[1]) if len(sys.argv)>1 else 200
    x,S,steps=30,[11,18,4],1607        # real level start at step 1607: 1 |30| 11 |18| 4
    t0=time.time()
    for lev in range(N):
        r=step(x,S)
        if r[0]=='HALT': print('HALT at level',lev); break
        x,S,st=r; steps+=st
        if lev<40 or lev%50==0: print(lev+1,'step',steps if steps<10**15 else '10^%d'%(len(str(steps))-1),'x',x if x<10**12 else '%d digits'%len(str(x)),'S',S[:14],'len',len(S),flush=True)
    print('rules',STATS,'time %.1f s'%(time.time()-t0))
