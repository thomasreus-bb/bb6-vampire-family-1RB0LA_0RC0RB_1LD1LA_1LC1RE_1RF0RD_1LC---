# watch70.py - long-running simulator for no. 70 (1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE) that improves the estimate
# of the halting rate step by step and judges whether the machine probably halts some day.
#
# What it does, in rounds (default: one round = 15 minutes, option --minutes):
#  1. continues the REAL macro run (exact x, rules from macro70.py, learned on the fly) for about 80 % of the round;
#     counts per window of 10,000 levels: new odd stack blocks of size 9 and less, levels that touch odd blocks < 13,
#     every shrink of an odd block (b -> b-2) near the front, and HALT (then it stops and reports the HALT);
#  2. uses the rest of the round for injection tests: in the current real stack an odd block v (1, 3, 5, 7, 9) is put
#     at one of the first three block positions, then W = 300 levels are run with coin-flip parities; counted are
#     "smaller odd block appears" (v -> v-2 or less) and HALT;
#  3. writes a report (watch70_report.txt) and a checkpoint (watch70_state.pkl, rules in rules70.pkl); a restart
#     continues from the checkpoint.
# Estimate:  rate per level = c_9 * P(HALT | 9),  P(HALT | v) = q_v * P(HALT | v-2),  P(HALT | 1) = h1,
#   c_9 = rate at which blocks 9 appear among the first three stack blocks (real run; blocks 1..7 arise from them), q_v = P(v -> v-2 within W levels), h1 = P(HALT within W | block 1).
#   Uncertainty: 5 / 50 / 95 % quantiles by sampling (Gamma for counts, Beta(k+1/2, n-k+1/2) for probabilities).
# Stationarity: slope of log(rate of dangerous levels) against log(level) over the windows (least squares).
#   slope > -0.5: rate about constant -> "HALT expected" (median levels = ln 2 / rate);
#   slope < -1:   rate falls faster than 1/N -> "convergent lottery, probably never halts";
#   otherwise:    undecided.
# This is a heuristic estimate, not a proof.
#
# usage:  python3 watch70.py [--minutes 15] [--rounds 1000000] [--fresh]
# needs:  macro70.py and lev70.c in the same folder (lev70 is compiled automatically; gcc required)
import sys,os,time,pickle,random,math,argparse
sys.set_int_max_str_digits(0)
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0,HERE)
import macro70
from macro70 import rule,RULES,STATS
ap=argparse.ArgumentParser(); ap.add_argument('--minutes',type=float,default=15); ap.add_argument('--rounds',type=int,default=10**6)
ap.add_argument('--fresh',action='store_true'); ap.add_argument('--seed',type=int,default=1)
A=ap.parse_args(); random.seed(A.seed)
CK='watch70_state.pkl'; REP='watch70_report.txt'; RF='rules70.pkl'
if os.path.exists(RF): RULES.update(pickle.load(open(RF,'rb')))
ODD=(1,3,5,7,9); W=300; WIN=10000

# ---------- fast stack: the stack is stored reversed (front = end of the list) ----------
def front(R,k):
    return R[:-k-1:-1] if len(R)>k else R[::-1]
def fastrule(x,R):
    k=18
    while True:
        P=front(R,k); whole=len(P)==len(R)
        r=rule(x,P)
        if r[0]=='HALT': return r
        if r[4] and not whole: k*=4; continue          # rule reaches the end of P but P is not the whole stack
        return r
def apply(x,R,r):
    """apply rule r; R is changed in place; returns x' (or None for HALT)"""
    if r[0]=='HALT': return None
    _,lp,fits,sf,inf=r
    a,b=fits[0]
    xn=(a.numerator*b.denominator*x+b.numerator*a.denominator)//(a.denominator*b.denominator)
    vals=[int(bb) for aa,bb in fits[1:]]                  # all other entries do not depend on x (checked when learned)
    if inf: del R[:]
    else: del R[len(R)-lp:]
    # vals = new prefix (m, g1, b1, ..., and the new gap before the untouched part if not inf)
    seq=vals
    # merge zero gaps: seq is [m, g, b, g, b, ...(, g)]; build front part, then join with R
    out=[seq[0]]; i=1
    while i+1<len(seq):
        g,bb=seq[i],seq[i+1]
        if g==0: out[-1]+=bb
        else: out+=[g,bb]
        i+=2
    if i<len(seq):                     # trailing gap before the untouched part
        g=seq[i]
        if g==0 and R:                 # join with the next untouched block
            nb=R.pop(); out[-1]+=nb
        else: out.append(g)
    R.extend(reversed(out))
    return xn
def oddfront(R,n=40):
    return [b for b in front(R,n)[2::2] if b%2 and b<=9]

# ---------- state ----------
if os.path.exists(CK) and not A.fresh:
    st=pickle.load(open(CK,'rb'))
else:
    st=dict(level=0,x=30,R=[4,18,11],win={},inj={v:[0,0,0] for v in ODD},created={v:0 for v in ODD},halt=None,rounds=0,seconds=0.0,min_odd=10**9)
# win[k] = [dangerous levels, new odd<=9 blocks] in window k (levels k*WIN ...)

def real_run(seconds):
    t0=time.time(); x=st['x']; R=st['R']; lev=st['level']
    while time.time()-t0<seconds:
        for _ in range(200):
            before=oddfront(R,8)
            r=fastrule(x,R); lp=r[1] if r[0]=='OK' else 0
            pre=[b for b in front(R,lp)[2::2] if b%2 and b<13] if lp else []
            xn=apply(x,R,r)
            lev+=1
            if xn is None:
                st['halt']=lev; st['x']=x; st['R']=R; st['level']=lev; return
            x=xn
            after=oddfront(R,8)
            k=lev//WIN; w=st['win'].setdefault(k,[0,0])
            post=[b for b in front(R,lp+4)[2::2] if b%2 and b<13]
            if pre or post: w[0]+=1
            # new or shrunk small odd blocks near the front (multiset difference)
            for v in ODD:
                d=after.count(v)-before.count(v)
                if d>0:
                    w[1]+=d; st['created'][v]+=d
                    st.setdefault('first',{}).setdefault(v,lev); st.setdefault('last',{})[v]=lev
                st['min_odd']=min([st['min_odd']]+after)
    st['x']=x; st['R']=R; st['level']=lev

def coin_level(x_res,R):
    xf=60+x_res+12*random.randint(0,3)
    r=fastrule(xf,R)
    return apply(xf,R,r)

def injections(seconds):
    t0=time.time()
    while time.time()-t0<seconds:
        v=random.choice(ODD); R=st['R'][:]
        pos=random.randint(1,3)                 # block b_pos (front index 2*pos)
        if len(R)<2*pos+1: continue
        R[len(R)-1-2*pos]=v
        smaller=False; halted=False
        for l in range(W):
            if coin_level(random.choice((0,6)),R) is None: halted=True; break
            if any(b<v for b in oddfront(R,2*pos+40)): smaller=True
        c=st['inj'][v]; c[0]+=1; c[1]+=smaller; c[2]+=halted

def quantiles(samples):
    s=sorted(samples); n=len(s); return s[int(0.05*n)],s[n//2],s[int(0.95*n)]
def estimate():
    lev=max(st['level'],1); N=4000; rates=[]
    for _ in range(N):
        # P(HALT | v) chain
        ph={}
        n,k1,h=st['inj'][1]; ph[1]=random.betavariate(h+0.5,n-h+0.5) if n else random.random()
        for v in (3,5,7,9):
            n,k,h=st['inj'][v]
            q=random.betavariate(k+0.5,n-k+0.5) if n else random.random()
            ph[v]=q*ph[v-2]
        # entry point: blocks 9 appearing near the front (smaller odd blocks arise from them by shrinking; their own
        # appearances are part of the chain and are not added again)
        c=random.gammavariate(st['created'][9]+0.5,1.0)/lev
        rate=c*ph[9]
        rates.append(rate)
    return quantiles(rates)
def slope():
    ks=sorted(k for k in st['win'] if k>0 and (k+1)*WIN<=st['level'])
    pts=[(math.log((k+0.5)*WIN),math.log(st['win'][k][0]+0.5)) for k in ks]
    if len(pts)<4: return None
    mx=sum(p[0] for p in pts)/len(pts); my=sum(p[1] for p in pts)/len(pts)
    sxx=sum((p[0]-mx)**2 for p in pts); sxy=sum((p[0]-mx)*(p[1]-my) for p in pts)
    b=sxy/sxx; res=[p[1]-my-b*(p[0]-mx) for p in pts]
    se=math.sqrt(sum(r*r for r in res)/max(1,len(pts)-2)/sxx)
    return b,se
def report():
    lo,me,hi=estimate(); sl=slope(); lev=st['level']
    lines=[]
    lines.append('=== round %d, %.1f h total, level %d (x has %d digits, stack %d entries, rules %d)'%(
        st['rounds'],st['seconds']/3600,lev,len(str(st['x'])),len(st['R']),len(RULES)))
    if st['halt']: lines.append('*** HALT in the real run at level %d ***'%st['halt'])
    lines.append('real run: new small odd blocks near the front %s; smallest odd block seen %s'%(st['created'],st['min_odd'] if st['min_odd']<10**9 else '-'))
    fi=st.get('first',{}); la=st.get('last',{})
    lines.append('closest approach (like D for the vampires): smallest odd block near the front %s; first/last level seen: %s'%(min(fi) if fi else '-', {v:(fi[v],la[v]) for v in sorted(fi)}))
    lines.append('injections (runs, smaller odd block appeared, HALT): %s'%({v:tuple(c) for v,c in st['inj'].items()}))
    lines.append('halting rate per level: 5%% %.2e, median %.2e, 95%% %.2e'%(lo,me,hi))
    n1=st['created'][1]; h=st['inj'][1]
    if h[0]: lines.append('  direct check: blocks 1 seen near the front %d times in %d levels -> rate < %.1e (95 %%) * P(HALT|1) %.3f = %.1e'%(n1,lev,(n1+3)/lev,h[2]/h[0],(n1+3)/lev*h[2]/h[0]))
    if me>0:
        for p,lab in ((lo,'low'),(me,'median'),(hi,'high')):
            if p>0: lines.append('  %-6s rate: 50 %% HALT after %.2e levels, 99 %% after %.2e levels (about 10^(%.2e) steps)'%(lab,math.log(2)/p,math.log(100)/p,0.352*math.log(2)/p))
    if sl:
        b,se=sl
        verdict='rate about constant -> HALT expected (in the model)' if b-2*se>-0.5 else ('rate falls faster than 1/N -> convergent lottery, probably never halts' if b+2*se<-1 else 'undecided (trend not clear yet)')
        lines.append('stationarity: slope of log(dangerous levels per window) vs log(level) = %.3f +- %.3f  => %s'%(b,se,verdict))
    else: lines.append('stationarity: not enough windows yet')
    txt='\n'.join(lines); print(txt,flush=True)
    open(REP,'a').write(txt+'\n')
def save():
    pickle.dump(st,open(CK+'.tmp','wb')); os.replace(CK+'.tmp',CK)
    pickle.dump(dict(RULES),open(RF+'.tmp','wb')); os.replace(RF+'.tmp',RF)

for rnd in range(A.rounds):
    T=A.minutes*60; t0=time.time()
    real_run(0.8*T)
    if st['halt']: st['rounds']+=1; st['seconds']+=time.time()-t0; report(); save(); break
    injections(0.2*T)
    st['rounds']+=1; st['seconds']+=time.time()-t0
    report(); save()
