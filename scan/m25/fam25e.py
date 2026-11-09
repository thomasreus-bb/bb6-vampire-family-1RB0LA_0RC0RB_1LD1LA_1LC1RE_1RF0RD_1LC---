# no. 25, wider family: D tapes 10 1^N T and A tapes (110)^a 100 1^b T with N up to 5000, up to 5 tail entries of up to 300 ones
import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import random,subprocess,sys,collections,re
M='1RB0LE_1LC0RD_0RA1LD_0LC1RA_1LF1LA_---1LA'
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2]); c=collections.Counter()
Dfam=re.compile(r'^101+(01+)*$')
for t in range(T):
    tl=''.join('0'+'1'*rnd.randrange(1,300) for _ in range(rnd.randrange(0,6)))
    if t%2: N=rnd.randrange(5,5000); tape='10'+'1'*N+tl; q='D'
    else: tape='110'*rnd.randrange(0,1500)+'100'+'1'*rnd.randrange(0,3000)+tl; q='A'
    r=subprocess.run(['./bsim',M,q,tape,'4000000000','D'],capture_output=True,text=True).stdout.split()
    if r[0]=='REC':
        out=r[2] if len(r)>2 else ''
        c['REC_in' if (Dfam.match(out) or len(out)>=200) else 'REC_out']+=1
    else:
        c[r[0]]+=1
        if r[0]=='HALT': print('HALT',q,tape[:80],r,flush=True)
print(dict(c),flush=True)
