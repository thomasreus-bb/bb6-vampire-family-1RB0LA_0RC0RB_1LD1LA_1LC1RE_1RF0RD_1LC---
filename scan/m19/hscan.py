import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
TM='1RB0LC_1LA1RE_1LD1RE_1RE0LA_0RA1RF_0RB---'
def run(a):
    j,T,r=a; L='110'+'1'*j+'0'; n=4*((40*len(L)+2000)//4)+r
    o=subprocess.run(['./bstep',TM,'R','E','1',L,T,str(n),'1.3',str(4*len(L)+400),'4000000000000'],capture_output=True,text=True).stdout.split()
    return (j,T,r,o[0],o[1] if len(o)>1 else '')
jobs=[(j,T,r) for j in range(0,int(sys.argv[1])) for T in ('0','010') for r in range(4)]
with ThreadPoolExecutor(2) as ex:
    res=list(ex.map(run,jobs))
from collections import Counter
print(Counter(x[3] for x in res))
for x in res:
    if x[3]!='OK': print(x)
