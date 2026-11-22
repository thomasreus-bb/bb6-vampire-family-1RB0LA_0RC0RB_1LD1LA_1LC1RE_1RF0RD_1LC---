// events: given state at a new rightmost cell; print the ones-blocks (left to right) and the zero runs between them
// argv: table start-state event-state steps [maxblocks]
#include <stdio.h>
#include <stdlib.h>
#define W (1<<25)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
int q=v[2][0]-'A',eq=v[3][0]-'A';long long N=atoll(v[4]);int MB=c>5?atoi(v[5]):30;int p=W/2,lo=p,hi=p;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<lo){lo=p;if(q==eq){printf("L%lld:",st+1);int x=p+1,n=0;while(x<=hi&&n<MB){if(t[x]==0){int z=0;while(x<=hi&&t[x]==0){z++;x++;} if(z>1&&n)printf(" |%d|",z);continue;}long L=0;while(x<=hi&&t[x]){L++;x++;}printf(" %ld",L);n++;}printf("\n");}}
 if(p>hi){hi=p;if(q==eq){printf("%lld:",st+1);int x=lo,n=0;while(x<p&&n<MB){if(t[x]==0){int z=0;while(x<p&&t[x]==0){z++;x++;} if(z>1&&n)printf(" |%d|",z);continue;}long L=0;while(x<p&&t[x]){L++;x++;}printf(" %ld",L);n++;}if(n>=MB)printf(" ...");printf("\n");}}
 if(p<2||p>W-3){printf("OVF %lld\n",st);return 0;}}}
