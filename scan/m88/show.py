import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import sys
exec(open('comp.py').read().split('for l in sys.stdin')[0])
for l in open(sys.argv[1]):
    f=l.split()
    if len(f)<4: print(l.strip()); continue
    print(f[0],f[1],f[2],len(f[3]),comp(f[3])[:int(sys.argv[2]) if len(sys.argv)>2 else 300])
