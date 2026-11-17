#include <stdio.h>
#include <stdlib.h>
#define W (1<<20)
static unsigned char t[W];static unsigned char snap[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long N=atol(v[2]);int *pos=malloc(sizeof(int)*N);char*qs=malloc(N);int p=W/2,q=0,lo=p,hi=p;
for(long st=0;st<N;st++){pos[st]=p;qs[st]=q;int b=t[p];t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<lo)lo=p;if(p>hi)hi=p;}
// suffix minima breakpoints
int m=1<<30; long *bt=malloc(sizeof(long)*200000);int *bp=malloc(sizeof(int)*200000);int nb=0;
for(long st=N-1;st>=0;st--){if(pos[st]<m){m=pos[st];bt[nb]=st;bp[nb]=m;nb++;}}
// print breakpoints whose wall persisted long: next breakpoint (to the right) happened much later
for(int i=nb-1;i>0;i--){long life=bt[i-1]-bt[i]; if(life>N/200) printf("wall at %d: last visit at step %ld (state %c), head stays right of it for %ld steps until the next wall\n",bp[i]-W/2,bt[i],'A'+qs[bt[i]],life);}
for(int x=lo;x<lo+400&&x<=hi;x++)putchar('0'+t[x]);putchar('\n');}
