// Start: state C on a 0 at the left end of  0 1^N 00 1^t  (blank elsewhere). Run to the next configuration
// of the same form (state C, head on a new leftmost cell, exactly two 1-blocks separated by 00).
// usage: ./syn TM N t [maxsteps]   prints  N' t' steps  or HALT steps
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long N=atol(v[2]),T=atol(v[3]);long long MX=c>4?atoll(v[4]):(long long)4e12;
int p=W/2,q=2,x=p+1;for(long i=0;i<N;i++)t[x++]=1;x+=2;for(long i=0;i<T;i++)t[x++]=1;
int lo=p,hi=x;
for(long long st=1;st<=MX;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p;
 if(p<lo){lo=p; if(q==2&&t[p]==0&&t[p+1]==1){int y=p+1;long a=0;while(t[y]==1){a++;y++;}
   if(t[y]==0&&t[y+1]==0&&t[y+2]==1){y+=2;long bb=0;while(t[y]==1){bb++;y++;} int z=hi;while(z>=y&&t[z]==0)z--; if(z<y){printf("%ld %ld %lld\n",a,bb,st);return 0;}}}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("MAX\n");}
