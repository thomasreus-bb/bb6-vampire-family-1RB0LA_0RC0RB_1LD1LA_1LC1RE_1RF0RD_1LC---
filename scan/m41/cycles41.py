# parse run41.py output (A events) into Bell cycles of no. 41
import sys,re
cyc=[]; cur=None
for line in open(sys.argv[1]):
    p=line.split(); st=int(p[1]); body=' '.join(p[2:])
    m=re.fullmatch(r'0 1 0 \(1\)\^(\d+)',body)
    if m:
        cur={'n':(int(m.group(1))-1)//2,'step':st,'ev':[],'lin':None}; cyc.append(cur); continue
    if cur is None: continue
    m=re.fullmatch(r'0 1 \(01\)\^(\d+) 0 \(1\)\^(\d+)',body)
    if m and cur['lin'] is None: cur['ev'].append((int(m.group(1)),int(m.group(2)))); continue
    m=re.fullmatch(r'0 \(1\)\^2 \(10\)\^(\d+) \(1\)\^(\d+)',body)
    if m and cur['lin'] is None: cur['lin']=(int(m.group(1)),int(m.group(2)))
for i,c in enumerate(cyc):
    ev=c['ev']; nd=0
    while nd+1<len(ev) and ev[nd+1]==(2*ev[nd][0]+5, ev[nd][1]-2*ev[nd][0]-8): nd+=1
    nb=len(ev)-1-nd
    x,y=c['lin'] if c['lin'] else (None,None)
    nxt=cyc[i+1]['n'] if i+1<len(cyc) else None
    pred=(x+2*y+2) if x is not None else None
    print(i+1, 'n=%d'%c['n'], 'doublings=%d'%(nd+1 if ev else 0), 'bounces=%d'%nb, 'A-start x=%s y=%s'%(x,y), 'next n=%s'%nxt, 'x+2y+2=%s'%pred, 'ratio=%.4f'%(nxt/c['n']) if nxt else '')
