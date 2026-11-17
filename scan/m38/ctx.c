#include <stdio.h>
#include <stdlib.h>
#define W (1<<22)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB0RE_1LC0RA_0LD0LB_1RE0LB_1RF---_0RB0RC";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long T[64];int n=c-1;for(int i=0;i<n;i++)T[i]=atoll(v[i+1]);int k=0;int p=W/2,q=0;
for(long long st=0;k<n;st++){ if(st==T[k]){printf("%lld ",st);for(int x=p-90;x<p;x++)putchar('0'+t[x]);putchar('\n');k++;}
 int b=t[p];t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];}}
