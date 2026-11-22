// no. 50: left-edge events in state E; tape = 0 1^a 0 1^b 0 1^c ... ; print only when the block list does not follow (a-2, b-2, c+6)
#include <stdio.h>
#include <stdlib.h>
#define W (1<<25)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB1RB_1LC0RE_---1LD_0RA1LB_1RA1LF_0LE1LE";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[1]);int p=W/2,q=0,lo=p,hi=p;long pr[3]={-9,-9,-9};int pn=-1;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p;
 if(p<lo){lo=p; if(q==4){long r[16];int n=0;int x=p;while(x<=hi&&n<16){if(t[x]==0){x++;continue;}long L=0;while(t[x]){L++;x++;} r[n++]=L;}
   if(n<=1) continue;
   int reg=(n==3&&pn==3&&r[0]==pr[0]-2&&r[1]==pr[1]-2&&r[2]==pr[2]+6);
   if(!reg){printf("%lld E:",st);for(int i=0;i<n;i++)printf(" %ld",r[i]);printf("   (zero runs:");x=p;int k=0;while(x<=hi&&k<20){long L=0;while(x<=hi&&t[x]==0){L++;x++;} if(x>hi)break; printf(" %ld",L);k++;while(t[x])x++;}printf(")\n");fflush(stdout);}
   pn=n;for(int i=0;i<3&&i<n;i++)pr[i]=r[i];}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}}
