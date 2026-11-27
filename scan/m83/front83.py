import subprocess,re,random,sys
from collections import Counter
rnd=random.Random(int(sys.argv[1])); T=int(sys.argv[2]); c=Counter(); ex={}
for it in range(T):
    nb=rnd.randint(1,6); S=''
    for i in range(nb):
        S+='1'*rnd.randint(1,30)
        if i<nb-1: S+='0'*rnd.randint(1,30)
    r=rnd.choice((1,2,3)); a=len(re.match(r'1+',S).group(0))
    N=rnd.randrange(4*len(S)+201,4*len(S)+500)
    o=subprocess.run(['./cyc83',str(N),str(r),S,'400000000'],capture_output=True,text=True).stdout.split()
    if o[0]=='HALT': k='HALT_front_ok' if a=={1:2,2:3,3:1}[r] else 'HALT_other'
    elif o[0]!='BELL': k=o[0]
    else:
        f=len(re.match(r'1+',o[3]).group(0))
        k='front>=5' if f>=5 else 'front<5'
        if a=={1:2,2:3,3:1}[r]: k='nohalt_but_halting_front'
    c[k]+=1; ex.setdefault(k,(N,r,S[:80]))
print(dict(c))
for k,v in ex.items():
    if k not in ('front>=5','HALT_front_ok'): print(k,v)
