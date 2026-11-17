// Real run: events "state E on a 0 with 1 to the left, then (10)^j X (10)^m 1 and blank", X in {0100,1100}.
// Print step, position, j, X, m, and the minimum head position since the previous event.
#include <stdio.h>
#include <stdlib.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB0RE_1LC0RA_0LD0LB_1RE0LB_1RF---_0RB0RC";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[1]);int p=W/2,q=0,hi=p,minp=p;long long lastev=-10;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p;if(p<minp)minp=p;
 if(q==4&&t[p]==0&&t[p-1]==1){int y=p+1,j=0;while(t[y]==1&&t[y+1]==0){j++;y+=2;}
   if(j>=1&&t[y+1]==1&&t[y+2]==0&&t[y+3]==0){int X=t[y];int y2=y+4;long mm=0;while(t[y2]==1&&t[y2+1]==0){mm++;y2+=2;}
     if(mm>=1&&t[y2]==0&&t[y2+1]==0&&y2>=hi){if(st-lastev!=4)printf("%lld pos %d j %d X %s m %ld minpos %d\n",st,p-W/2,j,X?"1100":"0100",mm-1,minp-W/2);fflush(stdout);if(st-lastev!=4)minp=p;lastev=st;}}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}}
