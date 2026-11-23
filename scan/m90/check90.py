# compare the DeepMind map of no. 90 with a direct TM simulation:
# every time state E reads 0 with well-formed stacks on both sides,
# record (a, L, d, R); the map states must appear in this sequence in order.
import subprocess, sys
from dm90 import step
T = '1RB1LB_1LC1LA_1RD0LB_1RA1RE_1RF0RD_---1RD'
src = r'''
#include <stdio.h>
#include <stdlib.h>
#define W (1<<25)
static unsigned char t[W];
/* parse blocks from position y in direction dir; returns count, -1 if malformed */
static int parse(int y,int dir,int lo,int hi,int*out){int n=0;
 for(;;){int k=0;while(y>=lo&&y<=hi&&t[y]){k++;y+=dir;}
  if(k==0) return -1; out[n++]=k-1;
  /* y is on a 0 (or outside) */
  int z=y+dir; if(z<lo||z>hi) return n;
  if(!t[z]){ /* 00: rest must be blank */ for(int w=z;w>=lo&&w<=hi;w+=dir) if(t[w]) return -1; return n;}
  y=z; if(n>900000) return -1;}}
static int Lb[1000000],Rb[1000000];
int main(int c,char**v){const char*s="%s";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[1]);int p=W/2,q=0,lo=p,hi=p;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT\n");return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<lo)lo=p;if(p>hi)hi=p;
 if(q==4&&t[p]==0&&t[p-1]&&t[p+1]){int nl=parse(p-1,-1,lo,hi,Lb),nr=parse(p+1,1,lo,hi,Rb);
  if(nl>0&&nr>0){printf("%%lld |",st+1);for(int i=0;i<nl;i++)printf(" %%d",Lb[i]);printf(" |");
   for(int i=0;i<nr;i++)printf(" %%d",Rb[i]);printf("\n");}}}}
''' % T
open('/tmp/sim90raw.c', 'w').write(src)
subprocess.run(['gcc', '-O2', '-o', '/tmp/sim90raw', '/tmp/sim90raw.c'], check=True)
out = subprocess.run(['/tmp/sim90raw', sys.argv[1]], capture_output=True, text=True).stdout.split('\n')
real = []
for l in out:
    if not l or not l[0].isdigit(): continue
    _, ls, rs = l.split('|')
    lv = list(map(int, ls.split())); rv = list(map(int, rs.split()))
    real.append((lv[0], tuple(lv[1:]), rv[0], tuple(rv[1:])))
st = (1, [], 0, []); seq = []
while st is not None and len(seq) < len(real) + 5:
    seq.append((st[0], tuple(st[1]), st[2], tuple(st[3]))); st = step(*st)
j = 0; ok = 0
for s in seq:
    while j < len(real) and real[j] != s: j += 1
    if j == len(real): break
    ok += 1; j += 1
print('real E-events', len(real), 'map states', len(seq), 'found in order:', ok)
# diagnostics: is the first unmatched map state simply beyond the simulated horizon?
j = 0; last = -1
for k, s in enumerate(seq):
    jj = j
    while jj < len(real) and real[jj] != s: jj += 1
    if jj == len(real):
        print('first unmatched map state #%d, last matched real index %d of %d' % (k, last, len(real)))
        print(' unmatched state sizes |L|=%d |R|=%d a=%d d=%d' % (len(s[1]), len(s[3]), s[0], s[2]))
        print(' last real event sizes', len(real[-1][1]), len(real[-1][3]))
        break
    last = jj; j = jj + 1
