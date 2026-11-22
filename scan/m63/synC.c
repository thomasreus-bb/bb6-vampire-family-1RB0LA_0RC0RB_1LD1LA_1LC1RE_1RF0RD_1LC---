// C(a,b,c,d) = 0^inf 1^(a+1) C> 0 0 1^(b+4) (01)^c 1^d 011 0^inf ; run to the next state C on 0 with "00" here and only ones to the left; print the right part
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W (1<<22)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long A=atol(v[2]),B=atol(v[3]),Cc=atol(v[4]),D=atol(v[5]);long long MX=atoll(v[6]);
int p=W/2;int x=p-1;for(long i=0;i<A+1;i++)t[x--]=1; int lo=x;x=p+2;for(long i=0;i<B+4;i++)t[x++]=1;for(long i=0;i<Cc;i++){t[x++]=0;t[x++]=1;}for(long i=0;i<D;i++)t[x++]=1;t[x++]=0;t[x++]=1;t[x++]=1;int hi=x;int q=2;
for(long long st=1;st<=MX;st++){int r=t[p];if(tq[q][r]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][r];p+=td[q][r];q=tq[q][r];if(p<lo)lo=p;if(p>hi)hi=p;
 if(q==2&&t[p]==0&&t[p+1]==0&&t[p-1]==1){int y=p-1;while(t[y])y--;int ok=1;for(int z=lo;z<y;z++)if(t[z]){ok=0;break;}
  if(ok){int z=hi;while(t[z]==0)z--;printf("%lld %d ",st,p-1-y);for(int k=p+2;k<=z;k++)putchar('0'+t[k]);putchar('\n');return 0;}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("MAX\n");}
