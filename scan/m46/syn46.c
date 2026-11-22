// Start: state E on the first cell of (01)^N, blank elsewhere. Run to the next event (E on a new leftmost cell, tape exactly (01)^N').
#include <stdio.h>
#include <stdlib.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB---_1RC1LE_0RD0RF_0RE0LA_1LF0LB_1LA1LD";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long N0=atol(v[1]);long long MX=atoll(v[2]);int p=W/4,x=p;for(long i=0;i<N0;i++){t[x]=0;t[x+1]=1;x+=2;}
int lo=p,hi=x,q=4;
for(long long st=1;st<=MX;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p;
 if(p<lo){lo=p; if(q==4){int y=p;long n=0;while(t[y]==0&&t[y+1]==1){n++;y+=2;} int z=hi;while(z>=y&&t[z]==0)z--; if(z<y&&n>0){printf("%ld %lld\n",n,st);return 0;}}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("MAX\n");}
