// no. 18: at every jump of the left edge (after a long gap) print the tape as E 0^k (10)^n tail.
#include <stdio.h>
#include <stdlib.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB---_1LC0LD_0RF0LD_0LE0RA_0LC1RA_1RC1RD";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[1]);int p=W/2,q=0,lo=p,hi=p;long long last=-1;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];
 if(p<lo){lo=p; if(last>=0&&st-last>1500){int x=p,k=0;while(x<=hi&&t[x]==0){x++;k++;}int n=0;while(x+1<=hi&&t[x]==1&&t[x+1]==0){n++;x+=2;}
   printf("%lld state %c 0^%d (10)^%d tail ",st,'A'+q,k,n);for(;x<=hi;x++)putchar('0'+t[x]);putchar('\n');fflush(stdout);}
  last=st;}
 if(p>hi)hi=p; if(p<2||p>W-3){printf("OVF\n");return 0;}}
}
