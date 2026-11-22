// Discord notation: A(a) = E on 0, then (10)^(a-1) 1 ; B(a,b) = E on 0, then (10)^a 1100 (10)^(b-1) 1 (as in the real run).
// Run to the next such configuration (E on 0 at a new leftmost cell? -> any E on 0 with blank to the left) and print it in Discord notation.
#include <stdio.h>
#include <stdlib.h>
#define W (1<<22)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB0RF_0LC1RE_---1LD_1LE0LB_0RF0LD_1RD1RA";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long a=atol(v[1]);long b=atol(v[2]);long long MX=atoll(v[3]);
int p=W/2,x=p+1;
if(b<0){for(long i=0;i<a-1;i++){t[x]=1;t[x+1]=0;x+=2;}t[x++]=1;}
else{for(long i=0;i<a;i++){t[x]=1;t[x+1]=0;x+=2;}t[x++]=1;t[x++]=1;t[x++]=0;t[x++]=0;for(long i=0;i<b-1;i++){t[x]=1;t[x+1]=0;x+=2;}t[x++]=1;}
int lo=p,hi=x,q=4;
for(long long st=1;st<=MX;st++){int r=t[p];if(tq[q][r]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][r];p+=td[q][r];q=tq[q][r];if(p<lo)lo=p;if(p>hi)hi=p;
 if(q==4&&t[p]==0){int ok=1;for(int y=lo;y<p;y++)if(t[y]){ok=0;break;}
  if(ok){int y=p+1;long A=0;while(t[y]==1&&t[y+1]==0){A++;y+=2;}int z=hi+2;while(z>=y&&t[z]==0)z--;
   if(z<y){printf("A %ld %lld\n",A,st);return 0;}
   if(t[y]==1&&t[y+1]==1&&t[y+2]==0&&t[y+3]==0){y+=4;long B=0;while(t[y]==1&&t[y+1]==0){B++;y+=2;} if(z<y){printf("B %ld %ld %lld\n",A,B,st);return 0;}}}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("MAX\n");}
