// State A at the left of  0 1^a 00 1^b 00 1^c ; run up to MX steps; print HALT step or "ok"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W (1<<22)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long A=atol(v[2]),B=atol(v[3]),C=atol(v[4]);long long MX=atoll(v[5]);int Q=v[6][0]-'A';
int p=W/2,q=Q,x=p+1;for(long i=0;i<A;i++)t[x++]=1;x+=2;for(long i=0;i<B;i++)t[x++]=1;x+=2;for(long i=0;i<C;i++)t[x++]=1;
for(long long st=1;st<=MX;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("ok\n");}
