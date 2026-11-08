# check the macro map of no. 62 against direct simulation of built tapes
import re
from tsim import run
from macro62 import cycle
def parse(st):
    m=re.match(r'^0*?(1*)0((?:01)*)(11)?0$',st)
    return (len(m.group(1)),len(m.group(2))//2,1 if m.group(3) else 0) if m else None
bad=0;n=0
for c in range(0,5):
  for b in range(0,60):
    for t in (0,1):
      tape=[1]*c+[0]+[0,1]*b+([1,1] if t else [])+[0]
      want=cycle(c,b,t)
      if c>0: stop=lambda st,c=c: (lambda p: p and p[0]==c-1)(parse(st))
      else:   stop=lambda st: (lambda p: p and p[0]>=3 and p[1]==0)(parse(st))
      r=run(tape,stop=stop,maxs=10**6)
      got='HALT' if r[0]=='HALT' else (parse(r[2]) if r[0]=='REC' else 'MAX')
      n+=1
      if got!=want: bad+=1; print('MISMATCH',c,b,t,want,got)
print(n,'cases,',bad,'mismatches')
