# Behaviour fingerprint of a run: the set of tape "shapes" at the records in the second half of the run.
# A shape is the tape with every repetition of a short word (period 1..6, >= 3 times) replaced by (w)*.
import re,subprocess,collections,sys
def shape(s):
    s=s.strip('0') or '0'
    out=[];i=0;n=len(s)
    while i<n:
        best=None
        for per in range(1,11):
            w=s[i:i+per]
            if len(w)<per: break
            k=1
            while s[i+k*per:i+(k+1)*per]==w: k+=1
            if k>=3 and (best is None or k*per>best[1]*best[0]): best=(per,k)
        if best:
            per,k=best; w=s[i:i+per]
            # rotate w to a canonical rotation so that phase shifts do not matter
            out.append('(%s)*'%min(w[r:]+w[:r] for r in range(per))); i+=per*k
        else: out.append(s[i]); i+=1
    # merge neighbouring equal tokens
    m=[]
    for t in out:
        if m and m[-1]==t and t.endswith('*'): continue
        m.append(t)
    return ''.join(m)
def fingerprint(tm,q,N=100000000,every=1,maxw=30000):
    r=subprocess.run(['./recs',tm,q,str(N),str(every),str(maxw)],capture_output=True,text=True).stdout.split('\n')
    tapes=[l.split()[3] for l in r if l and l[0].isdigit() and len(l.split())>3 and not l.split()[3].startswith('W')]
    last=r[-2] if len(r)>1 else ''
    half=tapes[len(tapes)//2:]
    c=collections.Counter(shape(t) for t in half)
    return c,len(tapes),last
if __name__=='__main__':
    c,n,last=fingerprint(sys.argv[1],sys.argv[2],int(sys.argv[3]))
    print(n,last); 
    for s,k in c.most_common(8): print(k,s[:150])
