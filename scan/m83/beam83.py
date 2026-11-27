import sys,heapq,itertools; sys.path.insert(0,'/tmp/an83')
from halt83c import stepc
def score(S):
    s=0
    for i,x in enumerate(S[:7]):
        if i%2==1:
            if x==1: s+=4
            elif x in (3,5): s+=2
            elif x==2: s+=1
        else:
            if x<6: s+=6
            elif x%2: s+=1
    return s
def search(r,par,S,maxnodes,cut=14):
    cnt=itertools.count(); start=(r,par,tuple(S[:cut]))
    pq=[(-score(start[2]),next(cnt),start,0,1.0,())]; seen=set(); best=None
    n=0
    while pq and n<maxnodes:
        sc,_,(r,par,S),d,p,path=heapq.heappop(pq); n+=1
        if (r,par,S) in seen: continue
        seen.add((r,par,S))
        c0s=(101,103) if par else (100,102)
        for c0 in c0s:
            SS=S if len(S)%2 else S[:-1]
            res=stepc(r,c0,SS+(40,6,40,6))
            if res=='HALT': return ('HALT',d+1,p/len(c0s),path+((r,c0,SS[:7]),)),n
            if res=='ERR': continue
            r2,pars,o=res
            o=o[:-4] if len(o)>4 else o
            o=tuple(o[:cut])
            for p2 in pars:
                st=(r2,p2,o)
                if st not in seen:
                    heapq.heappush(pq,(-score(o)+0.05*(d+1),next(cnt),st,d+1,p/len(c0s)/len(pars),path+((r,c0,SS[:7]),)))
    top=sorted(seen,key=lambda st:-score(st[2]))[:8]
    return ('NONE',top),n
if __name__=='__main__':
    Lr=[l.split() for l in open('/tmp/an83/orb83.txt') if l.split()[0].isdigit()]
    for k in (1078,1000,900):
        p=Lr[k]; r=int(p[3]); S=[int(x[1:]) for x in p[4:]]
        res,n=search(r,1,S,int(sys.argv[1]))
        print(k,'nodes',n); 
        if res[0]=='NONE':
            for t in res[1]: print('   top',score(t[2]),t)
        elif res: 
            for st in res[3]: print('    ',st)
        sys.stdout.flush()
