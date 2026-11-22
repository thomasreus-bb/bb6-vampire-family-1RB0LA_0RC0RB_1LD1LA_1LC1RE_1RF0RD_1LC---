// X(a,c) = state E on the first cell of  00 1^a 0 1^c  (blank elsewhere). Run to the next X(a',c').
#include <stdio.h>
#include <stdlib.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[4];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long A=atol(v[1]),C=atol(v[2]);long long MX=atoll(v[3]);int p=W/4,x=p+2;for(long i=0;i<A;i++)t[x++]=1;x++;for(long i=0;i<C;i++)t[x++]=1;
int lo=p,hi=x,q=4;
for(long long st=1;st<=MX;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p;
 if(p<lo){lo=p; if(q==4&&t[p]==0&&t[p+1]==0&&t[p+2]==1){int y=p+2;long a=0;while(t[y]){a++;y++;} if(t[y]==0&&t[y+1]==1){y++;long cc=0;while(t[y]){cc++;y++;} int z=hi;while(z>=y&&t[z]==0)z--; if(z<y){printf("%ld %ld %lld\n",a,cc,st);return 0;}}}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("MAX\n");}
