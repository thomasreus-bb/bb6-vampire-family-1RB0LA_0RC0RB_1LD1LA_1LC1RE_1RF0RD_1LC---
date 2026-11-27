import subprocess,re,sys
from collections import defaultdict
def runs(s): return [len(m.group(0)) for m in re.finditer(r'0+|1+',s)]
TAIL='0'*22+'1'*10+'0'*30+'1'*6
def bell(r,S,N=903):
    o=subprocess.run(['./cyc83',str(N),str(r),S+TAIL,'400000000'],capture_output=True,text=True).stdout.split()
    if o[0]!='BELL': return o[0]
    rs=runs(o[3]); 
    # strip known tail runs (22,10,30,6) at end if intact
    t=[22,10,30,6]
    rest='T' if rs[-4:]==t else 'T?'
    body=rs[:-4] if rest=='T' else rs
    return (int(o[2]),tuple(body),rest)
r=int(sys.argv[1])
for a in (6,8,10,12,14,16,18,20,30):
    for g in (2,4,6,8,10,12,20):
        b=12
        S='1'*a+'0'*g+'1'*b
        print(r,a,g,b,'->',bell(r,S))
