# halting rate from perturbed real Bell starts: runs until the tape is G times as long, or HALT
import subprocess,random,sys,math,bisect
from concurrent.futures import ThreadPoolExecutor
cfg={
 '10':('1RB---_0RC0RD_1LD1RB_0LE0LC_1RA0LF_1LD1LE','C',lambda n,m:'1'*n+'01'*m+'00',[(1378,36),(1758,27),(2205,6),(2760,8),(3474,20),(4399,35),(7412,32)]),
 '11':('1RB1LB_1RC---_1LD1LF_1LE0LD_0LA1RF_1LC0RE','F',lambda n,m:'10'*m+'01'*n+'0',[(963,5),(1247,299),(1563,196),(3051,108),(3863,47),(5579,438)]),
 '16':('1RB1LF_1RC1RF_0LD1RE_---1LC_0RB1RE_1LA0LE','C',lambda n,m:'0'+'1'*n+'01'*m+'0',[(488,15),(648,15),(848,23),(1092,11),(1853,1),(2342,1),(3902,1)]),
}
key=sys.argv[1]; TM,st,mk,starts=cfg[key]; N=int(sys.argv[2]); random.seed(int(sys.argv[3])); G=float(sys.argv[4]); par=int(sys.argv[5]) if len(sys.argv)>5 else 2
jobs=[]
for i in range(N):
    n,m=random.choice(starts); jobs.append((n+random.randint(-30,30),m))
def run(j):
    cs=mk(*j)
    o=subprocess.run(['./accsim',TM,'2','4000000000000000000','0','1','4000000000',cs,st,str(int(G*len(cs)))],capture_output=True,text=True).stdout
    if not o.startswith('HALT'): return (o.split()[0],None)
    tape=o.splitlines()[1].split('|',1)[1]; cells=0
    for tok in tape.split():
        if tok=='[head]': continue
        b,_,c=tok.partition('^'); cells+=len(b)*(int(c) if c else 1)
    return ('HALT',cells/len(cs))
with ThreadPoolExecutor(par) as ex: res=list(ex.map(run,jobs))
h=[x[1] for x in res if x[0]=='HALT']
print(key,'runs',N,'halts',len(h),'other',[x[0] for x in res if x[0] not in ('HALT','SPAN')][:5])
bins=[1.5,2,3,5,8,13,20,30,1e9]; c=[0]*len(bins)
for x in h: c[bisect.bisect_left(bins,x)]+=1
print('growth factor at HALT:',list(zip(bins,c)))
