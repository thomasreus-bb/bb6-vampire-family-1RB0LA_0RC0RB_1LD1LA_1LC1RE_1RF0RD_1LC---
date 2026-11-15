// From E 0^6 (10)^n TAIL (head on the first 0, blank to the left) run to the next configuration
// "state E on a new leftmost cell, followed by 0^6 (10)^m tail'" and print m, tail', steps.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB---_1LC0LD_0RF0LD_0LE0RA_0LC1RA_1RC1RD";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long n=atol(v[1]);const char*tail=v[2];memset(t,0,W);
int p=W/2,q=4,x=p+6;for(long i=0;i<n;i++){t[x++]=1;t[x++]=0;}for(const char*a=tail;*a;a++)t[x++]=*a-'0';
int lo=p,hi=x;long long st=0;
for(;;st++){int b=t[p];if(tq[q][b]<0){printf("HALT after %lld steps\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p;
 if(p<lo){lo=p; if(q==4&&st>20){int y=p,k=0;while(y<=hi&&t[y]==0){y++;k++;} if(k==6){int m=0;while(t[y]==1&&t[y+1]==0&&y+1<=hi){m++;y+=2;}
   int z=hi;while(z>y&&t[z]==0)z--; if(z-y<60&&m>0){printf("%d ",m);for(;y<=z;y++)putchar('0'+t[y]);printf(" %lld\n",st+1);return 0;}}}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
}
