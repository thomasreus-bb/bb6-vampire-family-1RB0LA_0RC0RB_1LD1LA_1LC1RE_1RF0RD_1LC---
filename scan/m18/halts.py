import subprocess
from tails import name
def ev(n,t):
    r=subprocess.run(['./syn18',str(n),t],capture_output=True,text=True,timeout=60).stdout.split(); return r
res={}
for typ in 'SPQR':
    for k in (range(0,25) if typ!='S' else [0]):
        t={'S':'1','P':'0001'+'01'*k,'Q':'11'+'01'*k,'R':'0001'+'01'*k+'00001'}[typ]
        if typ=='R' and k==0: continue
        for n in range(1,90):
            r=ev(n,t)
            if r[0]=='HALT': res.setdefault((typ,k),[]).append(n)
            elif r[0]=='OVF' : res.setdefault((typ,k,'ovf'),[]).append(n)
for key in sorted(res): print(key, res[key][:20], '...' if len(res[key])>20 else '')
