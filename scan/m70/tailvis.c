// for each new maximum of "how far right the head goes" after step S0, print; also print last visit to each of the last K cells
#include <stdio.h>
#include <stdlib.h>
#define W (1<<24)
static unsigned char t[W];static long long lastv[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
int q=v[2][0]-'A';long long N=atoll(v[3]);int p=W/2,hi=p;
for(long long st=1;st<=N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT\n");return 0;}lastv[p]=st;t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p;}
int z=hi;while(!t[z])z--;printf("rightmost 1 at offset %d from start; last visits of the right cells (offset:last step):\n",z-W/2);
for(int x=z-90;x<=hi;x++)printf("%d:%d:%lld ",x-W/2,t[x],lastv[x]);printf("\n");}
