// one level of no. 70 from a level start: state A on a blank cell, then the tape "1 x m g1 b1 g2 b2 ..." (ones/zeros alternating).
// The last token may be followed by blank tape. LIMIT = index (in cells from the tape start) of the first cell the head must not reach
// (start of block b_{d+1}); -1 = no limit (blank to the right).
// Output: "OK steps maxpos z0 : blocks"  |  "HALT steps"  |  "OUT steps" (head reached LIMIT) | "MAX"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W (1<<22)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
int p=W/4;int base=p+1;int x=base;char*tok=strtok(v[1]," ");int one=1;while(tok){long n=atol(tok);for(long i=0;i<n;i++)t[x++]=one;one=!one;tok=strtok(NULL," ");}
long lim=atol(v[2]);long long MX=atoll(v[3]);int lo=p,hi=x,q=0;long maxp=0;
for(long long st=1;st<=MX;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p; if(p-base>maxp)maxp=p-base; if(lim>=0&&p-base>=lim){printf("OUT %lld\n",st);return 0;}
 if(p<lo){lo=p; if(q==0){int y=p+1;while(y<=hi&&!t[y])y++; long z0=y-p-1;
   int y2=y+1;while(y2<=hi&&!t[y2])y2++;int L2=0;while(y2+L2<=hi&&t[y2+L2])L2++;
   if(t[y]&&!t[y+1]&&y<hi&&!(y2-y-1==6&&L2==4)){printf("OK %lld %ld %ld %ld :",st,maxp,z0,(long)(y-base));int k=0;while(y<=hi){long L=0;int bb=t[y];while(y<=hi&&t[y]==bb){L++;y++;} if(y>hi&&bb==0)break; printf(" %ld",L);k++;}printf("\n");return 0;}}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("MAX\n");}
