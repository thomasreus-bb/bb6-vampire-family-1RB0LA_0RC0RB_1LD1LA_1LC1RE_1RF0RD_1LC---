# experiments for no. 88: start the accelerated simulator from a (possibly modified) real phase start and record phases
import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import os,sys,random,math
os.environ['TM']='1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---'.translate(str.maketrans('LR','RL')); os.environ.setdefault('BS48','40')
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from rl import toks_to_rl
from build import make
from ph_desc import describe
class Done(Exception): pass
def phases(rl,q,K,cap=10**400):
    s=make(rl,q); out=[]; last=[None]
    def cb(s):
        d=describe([],0,s.R)
        if '[0]^' not in d: return
        pre,rest=d.split('[0]^',1)
        if '[' in pre or len(pre)>60: return
        g,far=rest.split(' ',1) if ' ' in rest else (rest,'')
        if far==last[0]: return
        last[0]=far; out.append((s.steps,chr(65+s.q),d))
        if len(out)>=K: raise Done()
    try: r=s.run(cap,cb)
    except Done: r='K'
    return r,s,out
def load(fn='ph88.txt'):
    L=[l for l in open(fn) if l.startswith('PH')]
    return L
def parse(l):
    f=l.split('|'); q=ord(l.split()[2])-65
    return q,toks_to_rl(f[1]+' '+f[2]+' '+f[3])
if __name__=='__main__':
    P=load(); i=int(sys.argv[1]); K=int(sys.argv[2])
    q,rl=parse(P[i])
    r,s,out=phases(rl,q,K)
    ok=0
    for j,(st,qq,d) in enumerate(out):
        try: q2,rl2=parse(P[i+1+j])
        except Exception: continue
        ok+= (toks_to_rl(d)==rl2 and q2==ord(qq)-65)
    print(r,'phases',len(out),'match',ok)
def far(rl):
    # the part after the main gap (the first zero run longer than 10^6... or the longest zero run)
    j=max(range(len(rl)),key=lambda k: rl[k][1] if rl[k][0]==0 else -1)
    return rl[j][1], rl[j+1:]
def fstr(f):
    return ' '.join(('%d'%n if n<10**5 else '%.3e'%n) if b==0 else '<%d>'%n for b,n in f)
