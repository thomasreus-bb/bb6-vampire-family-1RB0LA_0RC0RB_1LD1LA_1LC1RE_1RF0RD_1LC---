// count transition usage in step windows; argv: table steps
#include <stdio.h>
#include <stdlib.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[2]);int p=W/2,q=0;long long u[6][2]={0},last[6][2]={0};
for(long long st=1;st<=N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}u[q][b]++;last[q][b]=st;
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<2||p>W-3){printf("OVF\n");return 0;}}
for(int i=0;i<6;i++)for(int b=0;b<2;b++)printf("%c%d: %lld uses, last at step %lld\n",'A'+i,b,u[i][b],last[i][b]);}
