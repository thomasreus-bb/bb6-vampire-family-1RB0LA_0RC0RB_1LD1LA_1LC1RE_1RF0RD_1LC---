// no. 55: C(a,b) = 0^inf 110 A> 11^a 0 1^b 0^inf. Run to the next C(a',b') (state A, left part exactly 110).
#include <stdio.h>
#include <stdlib.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB1LF_0RC1RD_1LA1LD_1LE0RA_---1LC_0LA1LA";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long A=atol(v[1]),B=atol(v[2]);long long MX=atoll(v[3]);int base=W/4;t[base]=1;t[base+1]=1;t[base+2]=0;int p=base+3,x=p;
for(long i=0;i<2*A;i++)t[x++]=1;x++;for(long i=0;i<B;i++)t[x++]=1;
int lo=base,hi=x,q=0;
for(long long st=1;st<=MX;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<lo)lo=p;if(p>hi)hi=p;
 if(q==0&&t[p-1]==0&&t[p-2]==1&&t[p-3]==1){int ok=1;for(int y=lo;y<p-3;y++)if(t[y]){ok=0;break;}
  if(ok){int y=p;long n1=0;while(t[y]){n1++;y++;} if(n1%2==0&&t[y]==0&&t[y+1]==1){y++;long n2=0;while(t[y]){n2++;y++;} int z=hi;while(z>=y&&t[z]==0)z--; if(z<y){printf("%ld %ld %lld\n",n1/2,n2,st);return 0;}}}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("MAX\n");}
