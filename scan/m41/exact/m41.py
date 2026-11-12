# No. 41: 1RB1LD_1RC0RA_1LA1RE_0LA0LB_0RB1RF_---1RD.  macro configurations and exact single macro steps by direct simulation
import re,sys
TM='1RB1LD_1RC0RA_1LA1RE_0LA0LB_0RB1RF_---1RD'
T={}
for i,s in enumerate(TM.split('_')):
    for b in (0,1):
        x=s[3*b:3*b+3]; T[(i,b)]=None if x[0]=='-' else (int(x[0]),1 if x[1]=='R' else -1,ord(x[2])-65)
PAT=[('P1','B',re.compile(r'^(1*)\[0\]((?:10)*)(1+)$')),
     ('P2','A',re.compile(r'^(1*)0\[0\]((?:10)*)(1+)$')),
     ('P3','C',re.compile(r'^(1*)0((?:01)*)1\[0\](1+)$')),
     ('Q','C',re.compile(r'^(1+?)((?:01)*)1\[0\](1+)$')),
     ('A','B',re.compile(r'^\[0\]((?:01)*)(1*)$')),
     ('Bell','A',re.compile(r'^1((?:10)*)\[0\]$'))]
def start(kind,p):
    """tape string with head marker, state"""
    if kind=='P1': a,b,c=p; return '1'*a+'[0]'+'10'*b+'1'*c,1
    if kind=='P2': a,b,c=p; return '1'*a+'0[0]'+'10'*b+'1'*c,0
    if kind=='P3': a,b,c=p; return '1'*a+'0'+'01'*b+'1[0]'+'1'*c,2
    if kind=='Q': a,b,c=p; return '1'*a+'01'*b+'1[0]'+'1'*c,2
    if kind=='A': x,y=p; return '[0]'+'01'*x+'1'*y,1
    if kind=='Bell': (n,)=p; return '1'+'10'*n+'[0]',0
def classify(tape,pos,q):
    lo=min([k for k,v in tape.items() if v]+[pos]); hi=max([k for k,v in tape.items() if v]+[pos])
    s=''.join(('[%d]'%tape.get(i,0)) if i==pos else str(tape.get(i,0)) for i in range(lo,hi+1))
    for name,st,rx in PAT:
        if 'ABCDEF'[q]!=st: continue
        m=rx.match(s)
        if m:
            g=m.groups()
            if name in('P1','P2'): return name,(len(g[0]),len(g[1])//2,len(g[2]))
            if name in('P3','Q'): return name,(len(g[0]),len(g[1])//2,len(g[2]))
            if name=='A': return name,(len(g[0])//2,len(g[1]))
            return name,(len(g[0])//2,)
    return None
def step_macro(kind,p,maxsteps=2000000):
    s,q=start(kind,p); pos=s.index('['); s2=s.replace('[','').replace(']','')
    tape={i:1 for i,ch in enumerate(s2) if ch=='1'}
    for n in range(1,maxsteps+1):
        t=T[(q,tape.get(pos,0))]
        if t is None: return ('HALT',n)
        if t[0]: tape[pos]=1
        else: tape.pop(pos,None)
        pos+=t[1]; q=t[2]
        c=classify(tape,pos,q)
        if c: return c+(n,)
    return ('MAX',None)
if __name__=='__main__':
    # sanity: the Bell sequence 8, 28, 92, 300
    k,p=('Bell',(8,)); seq=[]
    for i in range(400):
        r=step_macro(k,p); 
        if r[0] in('HALT','MAX'): print(r); break
        k,p=r[0],r[1]
        if k=='Bell': seq.append(p[0])
        if len(seq)>=3: break
    print('Bells from 8:',seq)
