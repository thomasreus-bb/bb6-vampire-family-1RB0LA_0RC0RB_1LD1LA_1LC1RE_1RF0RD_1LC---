// no. 87: from (1100)^n TAIL E> (state E on the blank cell right of the tape), run to the next right-edge event in state E;
// print steps, n' (number of leading 1100 units) and the rest; or HALT / MAX
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W (1<<27)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB1LC_1RC0RF_1RD0LB_1RE0LD_1LF---_0RA1LA";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long n=atol(v[1]);const char*tail=v[2];long long MX=atoll(v[3]);
int lo=W/2,x=lo;for(long i=0;i<n;i++){t[x++]=1;t[x++]=1;t[x++]=0;t[x++]=0;}for(int i=0;tail[i];i++)t[x++]=tail[i]-'0';
int p=x,hi=x,q=4;
for(long long st=1;st<=MX;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<lo)lo=p;
 if(p>hi){hi=p;if(q==4){long k=0;int y=lo;while(y+3<p&&t[y]==1&&t[y+1]==1&&t[y+2]==0&&t[y+3]==0){k++;y+=4;}
   printf("%lld %ld ",st,k);for(;y<p;y++)putchar('0'+t[y]);putchar('\n');return 0;}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("MAX\n");}
