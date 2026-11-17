import subprocess,re
ctx='1'*40+'01'*10+'00'+'111'+'0101001'+'1'
for k in range(30):
    res={}
    for j in (200,201,202,203):
        r=subprocess.run(['./syn38c',str(j),'1',str(j//2),ctx],capture_output=True,text=True).stdout
        a=r.split('|')[0].split(); res[j]=(int(a[0]),int(a[1]),int(a[3]),r)
    d=[2*res[j][0]-5*j-(1 if j%2==0 else 0) for j in (200,201,202,203)]
    cont=[j%4 for j in (200,201,202,203) if res[j][1]==1]
    print('bell %d: delta %s, continue (1100) iff j mod 4 in %s, shift %s'%(k+1,sorted(set(d)),cont,sorted({res[j][2] for j in res})),flush=True)
    j=[j for j in res if res[j][1]==1][0]
    ctx='1'*40+re.search(r'1{20,}(.*)$',res[j][3].split('|')[1].strip()).group(1)
