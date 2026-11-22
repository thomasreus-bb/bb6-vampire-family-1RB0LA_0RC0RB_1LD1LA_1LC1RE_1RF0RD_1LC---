# accelerated run of no. 70 / 86 (mgen/msim.py, BS48=1): at every left-end event in state A (70) / B (86) parse the tape
# into blocks of ones and gaps, print the event whenever the "stack" (everything after the first gap) changes.
# usage: TM=... QEV=A python3 stack70.py seconds
import sys,os,re,signal
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'../mgen'))
os.environ.setdefault('BS48','1'); sys.set_int_max_str_digits(0)
from msim import Sim
from ph_desc import describe
QEV=ord(os.environ.get('QEV','A'))-65
def blocks(d):
    d=d.split('|')[-1] if '|' in d else d
    out=[]
    for tok in d.split():
        m=re.fullmatch(r'\[([01]+)\]\^(\d+)|([01])\^(\d+)|([01]+)',tok)
        if m.group(1): u,k=m.group(1),int(m.group(2))
        elif m.group(3): u,k=m.group(3),int(m.group(4))
        else: u,k=m.group(5),1
        if len(u)>1:
            for ch in u*min(k,4):
                out.append([int(ch),1])   # rare: multi-cell unit, only small repeats expected
            if k>4: out.append(['?',k])
            continue
        b=int(u)
        if out and out[-1][0]==b: out[-1][1]+=k
        else: out.append([b,k])
    return out
if __name__=='__main__':
    class Stop(Exception): pass
    def h(a,b): raise Stop()
    signal.signal(signal.SIGALRM,h); signal.alarm(int(sys.argv[1]))
    last=[None]; n=[0]; sizes={}
    def cb(s):
        if s.q!=QEV: return
        b=blocks(describe([],0,s.R))
        if not b or b[0][0]!=1 or len(b)<4: return
        ones=[k for v,k in b if v==1]; zer=[k for v,k in b if v==0]
        # stack = blocks of ones from the 3rd on, gaps from the 3rd on
        key=(tuple(ones[2:]),tuple(zer[2:]))
        for k in ones[2:]: sizes[k]=sizes.get(k,0)+1
        if key!=last[0]:
            n[0]+=1
            d=len(str(s.steps))
            print('step~10^%d  first=%s  gap=%s  m=%s | blocks %s | gaps %s'%(d-1,ones[0] if len(str(ones[0]))<9 else '%d digits'%len(str(ones[0])),
                  zer[0] if len(str(zer[0]))<9 else '%d digits'%len(str(zer[0])), ones[1] if len(ones)>1 else '-', ' '.join(map(str,ones[2:])),' '.join(map(str,zer[1:]))),flush=True)
            last[0]=key
    s=Sim()
    try: r=s.run(10**10**6,cb); print('RESULT',r,s.halt)
    except Stop: print('time up; step count has',len(str(s.steps)),'digits')
    print('block sizes in the stack (count over events):',sorted(sizes.items())[:40])

