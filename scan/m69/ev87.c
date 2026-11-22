// print edge events (new leftmost or rightmost cell) of a TM: state, side, tape compressed into (10)^k / (01)^k / bits
#include <stdio.h>
#include <stdlib.h>
#define W (1<<25)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[2]);int Q=v[3][0]-'A';char side=v[4][0];int p=W/2,q=0,lo=p,hi=p;long cnt=0;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];int ev=0;
 if(p<lo){lo=p;ev=(side=='L');} if(p>hi){hi=p;ev=(side=='R');}
 if(ev&&q==Q){printf("%lld:",st+1);int y=lo,n=0;
   while(y<=hi&&n<14){ if(y==p){printf(" [H]");y++;continue;}
     if(y+3<=hi&&t[y]==1&&t[y+1]==0&&t[y+2]==1&&t[y+3]==0){long k=0;while(y+1<=hi&&t[y]==1&&t[y+1]==0&&y!=p&&y+1!=p){k++;y+=2;}printf(" (10)^%ld",k);}
     else if(y+3<=hi&&t[y]==0&&t[y+1]==1&&t[y+2]==0&&t[y+3]==1){long k=0;while(y+1<=hi&&t[y]==0&&t[y+1]==1&&y!=p&&y+1!=p){k++;y+=2;}printf(" (01)^%ld",k);}
     else if(t[y]){long k=0;while(y<=hi&&t[y]&&y!=p){k++;y++;}printf(" 1^%ld",k);}
     else {long k=0;while(y<=hi&&!t[y]&&y!=p){k++;y++;}printf(" 0^%ld",k);}
     n++;}
   printf("\n"); if(++cnt>40)return 0;}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}}
