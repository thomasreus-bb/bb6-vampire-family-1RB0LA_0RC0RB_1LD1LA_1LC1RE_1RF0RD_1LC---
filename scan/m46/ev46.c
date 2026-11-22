// no. 46: left-edge events with state E and tape exactly (01)^N (head on the first 0)
#include <stdio.h>
#include <stdlib.h>
#define W (1<<25)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[2]);int Q=v[3][0]-'A';int p=W/2,q=0,lo=p,hi=p;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p;
 if(p<lo){lo=p; if(q==Q){int y=p;long n=0;while(y+1<=hi+1&&t[y]==0&&t[y+1]==1){n++;y+=2;} int z=hi;while(z>=y&&t[z]==0)z--; if(z<y&&n>0){printf("%lld E (01)^%ld\n",st,n);fflush(stdout);}}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}}
