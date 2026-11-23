// edge events of a TM in state Q at side L/R; tape written with units: U = 1100 repeated, other bits literally
#include <stdio.h>
#include <stdlib.h>
#define W (1<<26)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[2]);int Q=v[3][0]-'A';char side=v[4][0];const char*U=c>5?v[5]:"1100";int ul=0;while(U[ul])ul++;
int p=W/2,q=0,lo=p,hi=p;long cnt=0;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];int ev=0;
 if(p<lo){lo=p;ev=(side=='L');} if(p>hi){hi=p;ev=(side=='R');}
 if(ev&&q==Q){printf("%lld:",st+1);int y=lo;
   while(y<=hi){ if(y==p){printf(" [H]");y++;continue;}
     long k=0; while(y+ul-1<=hi){int ok=1;for(int j=0;j<ul;j++)if(t[y+j]!=U[j]-'0'||y+j==p)ok=0; if(!ok)break; k++; y+=ul;}
     if(k>=2){printf(" (%s)^%ld",U,k);continue;} if(k==1){printf(" %s",U);continue;}
     printf(" %d",t[y]); y++; }
   printf("\n"); if(++cnt>(c>6?atol(v[6]):30))return 0;}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}}
