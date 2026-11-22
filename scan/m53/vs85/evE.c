// print events: state E on a 0 at a new leftmost or rightmost tape cell (argv: table steps side L/R); tape compressed in (10) and (01) runs
#include <stdio.h>
#include <stdlib.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[2]);char side=v[3][0];int p=W/2,q=0,lo=p,hi=p;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];
 int nl=0; if(p<lo){lo=p;nl=(side=='L');} if(p>hi){hi=p;nl=(side=='R');}
 if(nl&&q==4){printf("%lld:",st);int y=lo,e=hi,d=1;if(side=='R'){y=hi;e=lo;d=-1;}
   y+=d; // skip head cell
   int n=0;while((d>0?y<=e:y>=e)&&n<60){ if(t[y]==1&&t[y+d]==0&&t[y+2*d]==1&&t[y+3*d]==0){long k=0;while(t[y]==1&&t[y+d]==0&&(d>0?y+d<=e:y+d>=e)){k++;y+=2*d;} printf(" (10)^%ld",k);} else {printf(" %d",t[y]);y+=d;} n++;}
   printf("\n");}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}}
