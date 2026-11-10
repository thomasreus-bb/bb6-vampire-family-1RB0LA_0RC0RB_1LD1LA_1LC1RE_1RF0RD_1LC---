# follow raw C-events of mirrored no. 73 from a tape, report forms
import subprocess,re,sys,random
from xm import M,sh
def step(tape):
    r=subprocess.run(['./xmap',M,tape,'5000000000'],capture_output=True,text=True).stdout.split()
    return (r[0], r[2] if len(r)>2 else None)
def form(s):
    m=re.match(r'00(1+)',s)
    if not m: return 'nolead'
    rest=s[2+len(m.group(1)):]
    if re.fullmatch(r'(01+)*',rest): return 'ok'
    return 'odd'
rnd=random.Random(1); stats={'back_ok':0,'halt':0,'still_odd':0}
cases=[(283,[2,3,2,2,2,2,8,5,59,3]),(91,[8,3,2,56,2,3]),(77,[12,2,3,5,2,2,5,2,5,2]),(22,[2,3,8,2,2,5,8,2,2]),(40,[8,3,2,54,2,2,2,3,3])]
for m,S in cases:
    tape='00'+'1'*m+''.join('0'+'1'*k for k in S)
    hist=[]
    for i in range(40):
        r,t=step(tape)
        if r!='X': hist.append(r); break
        f=form(t); hist.append(f)
        tape=t
        if f=='ok' and 'odd' in hist: break
    i0=hist.index('odd') if 'odd' in hist else -1
    print(m,sh(S),' '.join(hist[:20]))
    if i0>=0:
        pass
