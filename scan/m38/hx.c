// Start: left context ctx (preceded by 1^L), state E on [0], then (10)^j X (10)^m 1. Run up to MX steps; print HALT step or ok.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W (1<<22)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB0RE_1LC0RA_0LD0LB_1RE0LB_1RF---_0RB0RC";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long j0=atol(v[1]);const char*X=v[2];long m0=atol(v[3]);long long MX=atoll(v[4]);const char*ctx=v[5];
int w=W/4;int cl=strlen(ctx);for(int i=w-3000-cl;i<w-cl;i++)t[i]=1;for(int i=0;i<cl;i++)t[w-cl+i]=ctx[i]-48;
int x=w+1;for(long i=0;i<j0;i++){t[x]=1;t[x+1]=0;x+=2;}for(const char*a=X;*a;a++)t[x++]=*a-48;for(long i=0;i<m0;i++){t[x]=1;t[x+1]=0;x+=2;}t[x++]=1;
int p=w,q=4,minp=p;for(long long st=1;st<=MX;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld minoff %d\n",st,minp-w);return 0;}t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<minp)minp=p;if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("ok minoff %d\n",minp-w);}
