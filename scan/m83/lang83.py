import subprocess,re,random,sys
from collections import Counter
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2]); BMIN=int(sys.argv[3]); GMIN=int(sys.argv[4]); BMAX=int(sys.argv[5]); GMAX=int(sys.argv[6])
c=Counter(); ex={}
def runs(s): return [(m.group(0)[0],len(m.group(0))) for m in re.finditer(r'0+|1+',s)]
for it in range(T):
    nb=rnd.randint(1,6); S=''
    for i in range(nb):
        S+='1'*rnd.randint(BMIN,BMAX)
        if i<nb-1: S+='0'*rnd.randint(GMIN,GMAX)
    S+='0'*40+'1'*6   # sentinel tail block far away
    r=rnd.choice((1,2,3)); N=6*rnd.randrange((4*len(S)+201)//6,(4*len(S)+600)//6)+3
    o=subprocess.run(['./cyc83',str(N),str(r),S,'400000000'],capture_output=True,text=True).stdout.split()
    if o[0]!='BELL': k=o[0]
    else:
        rs=runs(o[3])
        bad=[x for x in rs[:-1] if (x[0]=='1' and x[1]<BMIN) or (x[0]=='0' and x[1]<GMIN)]
        k='closed' if not bad else 'OUT'
        if int(o[2]) not in (1,2,3): k='r'
    c[k]+=1
    if k!='closed': ex.setdefault(k,[]).append((N%24,r,' '.join(f'{a}{b}' for a,b in runs(S)), o[:3], ' '.join(f'{a}{b}' for a,b in runs(o[3]))[:90] if o[0]=='BELL' else ''))
print(dict(c))
for k,v in ex.items():
    for e in v[:4]: print(k,e)
