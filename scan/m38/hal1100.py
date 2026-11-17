import subprocess,re
def comp(s): return re.sub(r'(1|01|10)\1{2,}', lambda m: '(%s)^%d '%(m.group(1), len(m.group(0))//len(m.group(1))), s)
ctx='1'*40+'01'*10+'00'+'111'+'0101001'+'1'
ctxs=[ctx]
for k in range(7):  # build islands I0..I7 by forcing 1100 continuations
    for j in (200,201,202,203):
        r=subprocess.run(['./syn38c',str(j),'1',str(j//2),ctx],capture_output=True,text=True).stdout
        if not r.startswith('HALT') and r.split()[1]=='1':
            ctx='1'*40+re.search(r'1{20,}(.*)$',r.split('|')[1].strip()).group(1); ctxs.append(ctx); break
for k,c in enumerate(ctxs):
    H=[]
    for j in range(1,520):
        r=subprocess.run(['./hx',str(j),'1100',str(j//2),'30000000',c],capture_output=True,text=True).stdout
        if r.startswith('HALT'): H.append(j)
    isl=re.search(r'1{20,}(.*)$',c).group(1)
    print('bell %d, island %s: HALT at j = %s'%(k+1,comp(isl),H),flush=True)
