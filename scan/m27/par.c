// From C at left of 0 1^N 00 1^t, run MX steps; count left-edge events in state A where the tape is
// 0 1^a 00 ... and report how many have a odd (first example).
#include <stdio.h>
#include <stdlib.h>
#define W (1<<22)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long N=atol(v[2]),T=atol(v[3]);long long MX=atoll(v[4]);int Q=v[5][0]-'A';
int p=W/2,q=Q,x=p+1;for(long i=0;i<N;i++)t[x++]=1;x+=2;for(long i=0;i<T;i++)t[x++]=1;
int lo=p;long ev=0,odd=0;
for(long long st=1;st<=MX;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld ev %ld odd %ld\n",st,ev,odd);return 0;}t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];
 if(p<lo){lo=p;if(q==0&&t[p]==0&&t[p+1]==1){int y=p+1;long a=0;while(t[y]){a++;y++;} if(t[y+1]==0){ev++; if(a%2){odd++; if(odd==1)printf("  first odd: step %lld a=%ld\n",st,a);}}}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("ok ev %ld odd %ld\n",ev,odd);}
