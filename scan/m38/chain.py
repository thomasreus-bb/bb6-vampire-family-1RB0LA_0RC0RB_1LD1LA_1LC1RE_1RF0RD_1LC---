import subprocess,re
def comp(s): return re.sub(r'(1|01|10)\1{2,}', lambda m: '(%s)^%d '%(m.group(1), len(m.group(0))//len(m.group(1))), s)
ctx='1'*40+'01'*10+'00'+'111'+'0101001'+'1'
for k in range(40):
    res={}
    for j in (200,201,202,203):
        for X in (1,0):
            r=subprocess.run(['./syn38c',str(j),str(X),str(j//2),ctx],capture_output=True,text=True).stdout
            res[(j,X)]=r
    halts=[(jx,r.split()[1]) for jx,r in res.items() if r.startswith('HALT')]
    cont=[(jx,r) for jx,r in res.items() if jx[1]==1 and not r.startswith('HALT') and r.split()[1]=='1']
    isl=re.search(r'1{20,}(.*)$',ctx).group(1)
    print('k=%d island %s | halts: %s'%(k,comp(isl),halts))
    if not cont: print('no continuation with X=1100'); break
    (j,X),r=cont[0]; a,b=r.split('|'); ctx='1'*40+re.search(r'1{20,}(.*)$',b.strip()).group(1)
