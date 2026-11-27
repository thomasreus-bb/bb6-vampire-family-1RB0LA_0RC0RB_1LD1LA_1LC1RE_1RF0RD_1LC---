import sys; sys.path.insert(0,'/tmp/an83')
from halt83 import search
tail=[30,6,30,6,30,6]
import itertools
for a in (5,6,7,8,9):
  for b in (4,5,6):
    for r in (1,2,3):
      for par in (0,1):
        found=[]; search(r,par,[a,1,b]+tail,6,[],found)
        if found: print('a',a,'b',b,'r',r,'par',par,'HALT branches',len(found),'p=%.3g'%sum(p for _,p in found), found[0][0])
print('done')
