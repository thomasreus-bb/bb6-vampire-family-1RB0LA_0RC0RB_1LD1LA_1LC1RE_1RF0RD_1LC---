import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import sys,time,chain39 as c
c.USE2=True
tail=[8]; P=''
t0=time.time()
for stage in range(int(sys.argv[1])):
    big=max(tail) if tail else 1
    N=10**(len(str(big))+25)+1
    o=c.bell(P,N,tail)
    if o[0]=='HALT':
        print('stage',stage,'tail',tail,'-> HALT after',o[1],'steps',flush=True); break
    newtail=o[2][:-1] if o[2] and o[2][-1]==2 else o[2]
    import math
    f=max(newtail)/max(tail) if tail and newtail else 0
    print('stage %d  tail %s  ->  %s   factor %.4f = 1.5^%.2f   (%.0fs)'%(stage,tail if len(str(tail))<200 else '[%d counters, max %.4e]'%(len(tail),max(tail)),
          newtail if len(str(newtail))<200 else '[%d counters, max %.4e]'%(len(newtail),max(newtail)), f, math.log(f)/math.log(1.5) if f>0 else 0, time.time()-t0),flush=True)
    tail=newtail
    if not tail: print('tail vanished'); break
