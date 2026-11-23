# compare the DeepMind map of no. 104 with a direct simulation (state E reading 0 at the left end)
import subprocess,sys
from dm104 import step
T='1RB1RE_1LC1LB_1LE0LD_1LE1LC_0RF1RA_---1RA'
src=r'''
#include <stdio.h>
#include <stdlib.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s="%s";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[1]);int p=W/2,q=0,lo=p,hi=p;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT\n");return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<lo)lo=p;if(p>hi)hi=p;
 if(q==4&&t[p]==0&&p<=lo){int y=p+1;printf("%%lld",st+1);while(y<=hi){int k=0;while(y<=hi&&t[y]){k++;y++;} if(k==0)break; printf(" %%d",k-1);y++;}printf("\n");}}}
'''%T
open('/tmp/sim104.c','w').write(src)
subprocess.run(['gcc','-O2','-o','/tmp/sim104','/tmp/sim104.c'],check=True)
out=subprocess.run(['/tmp/sim104',sys.argv[1]],capture_output=True,text=True).stdout.split('\n')
real=[tuple(map(int,l.split()[1:])) for l in out if l and l[0].isdigit()]
st=(0,[0]); seq=[tuple([st[0]]+st[1])]
for _ in range(len(real)+5):
    st=step(*st)
    if st is None: break
    seq.append(tuple([st[0]]+st[1]))
# every map state must appear in the real sequence, in order
j=0; ok=0
for s in seq:
    while j<len(real) and real[j]!=s: j+=1
    if j==len(real): break
    ok+=1; j+=1
print('real events',len(real),'map states found in order:',ok)
print('first map states:',seq[:8])
