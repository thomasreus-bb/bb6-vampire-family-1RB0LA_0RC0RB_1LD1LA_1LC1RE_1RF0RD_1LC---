import subprocess,random,sys
from concurrent.futures import ThreadPoolExecutor
TM=sys.argv[1]; N=int(sys.argv[2]); G=int(sys.argv[3]); random.seed(7)
def run(i):
    n=random.randint(2000,20000); L=random.choice(['','10']); T=random.choice(['0','010'])
    cs=L+'1'*n+T
    o=subprocess.run(['./accsim',TM,'3','4000000000000000000','0','1','50000000',cs,'A',str(G*len(cs))],capture_output=True,text=True).stdout
    return o.split()[0]
with ThreadPoolExecutor(2) as ex: res=list(ex.map(run,range(N)))
from collections import Counter; print(Counter(res))
