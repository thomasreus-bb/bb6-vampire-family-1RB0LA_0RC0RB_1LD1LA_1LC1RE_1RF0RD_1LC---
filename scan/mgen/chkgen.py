import os,sys,random
sys.argv=['hitgen.py',sys.argv[1],'1','0','1','0','0','100',sys.argv[2]]
exec(open('hitgen.py').read())
from ph_desc import describe
i=int(os.environ['IDX']); l=L[i]; q=ord(l.split()[3])-65
s=make2(expand(parse(l),random.Random(0)),q); got=[]
def cb(s):
    if chr(65+s.q) in EVS and s.steps>0:
        got.append(chr(65+s.q)+' | '+describe([],0,s.R))
        if len(got)>=3: raise Done()
try: s.run(10**400,cb)
except Done: pass
for j,g in enumerate(got):
    ref=L[i+1+j].split(' ',3)[3].strip()
    print(g.strip()==ref.strip(), g[:120])
