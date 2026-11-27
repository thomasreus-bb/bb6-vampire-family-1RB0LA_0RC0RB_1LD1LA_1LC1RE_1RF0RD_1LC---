import subprocess,random,re,sys
from collections import Counter
TM='1LB1RF_1LC1RD_1RB1RE_1RE0RD_0RA0LE_1LD---'
L=[l.split() for l in open('/tmp/an/r78.txt')]
idx=int(sys.argv[1]); T=int(sys.argv[2]); seed=int(sys.argv[3]); mode=sys.argv[4]
s,q,t=L[idx]
lead=len(t)-len(t.lstrip('0'))
toks=[]
for m in re.finditer(r'(1+)(0*)',t[lead:]): toks.append(m.group(0))
def enc(tk): return '0'*lead+''.join(tk)
assert enc(toks)==t
rnd=random.Random(seed); res=Counter(); ex={}
for it in range(T):
    tk=list(toks)
    nm=rnd.randint(1,3)
    for j in range(nm):
        i=rnd.randrange(30,len(tk)-5)
        if mode=='add' and tk[i]=='100': tk[i]='1000'
        elif mode=='del':
            ds=[k for k in range(30,len(tk)) if tk[k]=='1000']
            if ds: tk[rnd.choice(ds)]='100'
        elif mode=='mix':
            if tk[i]=='100': tk[i]='1000'
            elif tk[i]=='1000': tk[i]='100'
    o=subprocess.run(['/tmp/an/synthev',TM,'E','0','3000000000','E'],input=enc(tk)+'\n',capture_output=True,text=True).stdout.split()
    res[o[0]]+=1
    if o[0]!='REC': ex.setdefault(o[0],[]).append((it,o[:3]))
    else: res['len%d'%(len(o[3])//1000)]+=1
print(idx,mode,dict(res)); print({k:v[:5] for k,v in ex.items()})
