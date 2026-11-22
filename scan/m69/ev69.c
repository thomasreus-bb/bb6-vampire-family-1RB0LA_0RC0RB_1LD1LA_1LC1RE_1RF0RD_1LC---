// no. 69: print configurations A(n+6,m) = 0^inf <C (10)^n 1^m 0^inf  (state C, head on the blank cell left of the tape)
#include <stdio.h>
#include <stdlib.h>
#define W (1<<26)
static unsigned char t[W];
int main(int c,char**v){const char*s=c>2?v[2]:"1RB1LE_0LC0LB_1RD1LC_1RD1RA_1RF0LA_---1RE";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[1]);int p=W/2,q=0,lo=p,hi=p;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<lo)lo=p;if(p>hi)hi=p;
 if(q==2&&p<=lo&&t[p]==0){int y=p+1;long n=0;while(t[y]==1&&t[y+1]==0&&(t[y+2]==1)){n++;y+=2;} // (10)^n then 1^m
   // careful: (10)^n followed by 1^m: last "10" must be followed by 1 (m>0) or blank
   long m=0;int z=y;while(t[z]){m++;z++;}
   int ok=1;for(int k=z;k<=hi;k++)if(t[k]){ok=0;break;}
   if(ok) printf("%lld: A(%ld,%ld)\n",st+1,n+6,m); else printf("%lld: other\n",st+1);}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}}
