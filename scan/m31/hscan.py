import sys
from probe import run
from concurrent.futures import ThreadPoolExecutor
ex=ThreadPoolExecutor(2)
pre=tuple(map(int,sys.argv[1].split(","))) if sys.argv[1]!="-" else ()
xs=range(int(sys.argv[2]),int(sys.argv[3]))
n0=int(sys.argv[4]) if len(sys.argv)>4 else 3240
res={}
for x in xs:
    fs=[ex.submit(run,pre+(x,),n0+r,0) for r in range(6)]
    h=[r for r,f in enumerate(fs) if f.result()[0]=="HALT"]
    if h: print("prefix",pre+(x,),"t=0 HALT for n mod 6 in",h,flush=True)
