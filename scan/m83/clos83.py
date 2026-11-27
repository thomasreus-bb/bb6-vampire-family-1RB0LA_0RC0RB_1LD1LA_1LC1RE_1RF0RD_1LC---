import subprocess,random,re,sys
random.seed(int(sys.argv[1])); T=int(sys.argv[2]); bmin=int(sys.argv[3]); gmin=int(sys.argv[4])
from collections import Counter
st=Counter(); ex={}
for it in range(T):
    nb=random.randint(1,7); S=''
    for i in range(nb):
        S+='1'*random.choice([2*random.randint(bmin//2,bmin//2+3), 2*random.randint(bmin//2,30)])
        if i<nb-1: S+='0'*random.choice([2*random.randint(gmin//2,gmin//2+3),2*random.randint(gmin//2,35)])
    r=random.choice((1,3)); N=random.choice(range(4*len(S)+201,4*len(S)+400,2))
    o=subprocess.run(['./cyc83',str(N),str(r),S,'400000000'],capture_output=True,text=True).stdout.split()
    if o[0]!='BELL': st[o[0]]+=1; ex.setdefault(o[0],(N,r,S)); continue
    runs=[(m.group(0)[0],len(m.group(0))) for m in re.finditer(r'0+|1+',o[3])]
    if any(l%2 for c,l in runs): k='ODD'
    elif any(c=='1' and l<bmin for c,l in runs): k='SHORTBLOCK'
    elif any(c=='0' and l<gmin for c,l in runs): k='SHORTGAP'
    elif int(o[2]) not in (1,3): k='R'
    else: k='OK'
    st[k]+=1
    if k!='OK': ex.setdefault(k,(N,r,S,o[3]))
print(dict(st));
for k,v in ex.items(): print(k,v)
