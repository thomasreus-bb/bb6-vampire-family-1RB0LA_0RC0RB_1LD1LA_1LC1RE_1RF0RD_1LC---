# closure check for no. 25: from D-family and A-family tapes, does the next D record stay in the D family 10 1^N (0 1^k)*?
import os as _o,sys as _s; _s.path.insert(0,_o.path.join(_o.path.dirname(_o.path.abspath(__file__)),'..','mgen'))
import random,subprocess,sys,collections,re
M='1RB0LE_1LC0RD_0RA1LD_0LC1RA_1LF1LA_---1LA'
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2]); c=collections.Counter(); bad=[]
Dfam=re.compile(r'^101+(01+)*$')
for t in range(T):
    tl=''.join('0'+'1'*rnd.randrange(1,80) for _ in range(rnd.randrange(0,4)))
    if t%2: tape='10'+'1'*rnd.randrange(1,2000)+tl; q='D'
    else: tape='110'*rnd.randrange(0,300)+'100'+'1'*rnd.randrange(0,600)+tl; q='A'
    r=subprocess.run(['./bsim',M,q,tape,'2000000000','D'],capture_output=True,text=True).stdout.split()
    if r[0]=='REC':
        out=r[2] if len(r)>2 else ''
        ok=bool(Dfam.match(out)) or len(out)>=200
        c['REC_in' if ok else 'REC_out']+=1
        if not ok: bad.append((q,tape[:60],out))
    else:
        c[r[0]]+=1
        if r[0]=='HALT': print('HALT from',q,tape,r)
print(c); print(bad[:5])
