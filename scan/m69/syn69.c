// no. 69: from A(N,m) = 0^inf <C (10)^(N-6) 1^m, run to the next A configuration; print it, HALT, or NONE (limit)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB1LE_0LC0LB_1RD1LC_1RD1RA_1RF0LA_---1RE";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long N=atol(v[1]),m=atol(v[2]);long long MX=atoll(v[3]);int p=W/2;int x=p+1;for(long i=0;i<N-6;i++){t[x++]=1;t[x++]=0;}for(long i=0;i<m;i++)t[x++]=1;
int q=2,lo=p,hi=x;
for(long long st=1;st<=MX;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<lo)lo=p;if(p>hi)hi=p;
 if(q==2&&p<=lo&&t[p]==0){int y=p+1;long n=0;while(t[y]==1&&t[y+1]==0&&t[y+2]==1){n++;y+=2;}
   long mm=0;int z=y;while(t[z]){mm++;z++;}int ok=1;for(int k=z;k<=hi;k++)if(t[k]){ok=0;break;}
   if(ok){ if(mm==1){n++;mm=0;} printf("%lld %ld %ld\n",st,n+6,mm);return 0;}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("NONE\n");}
