// Start: 1^L, state E on [0] at w, then (10)^j X (10)^m 1, blank. Run to the next event
// "E on 0 with 1 to the left, (10)^j' X' (10)^m' 1, end of tape", skipping fill events (4 steps after the previous one).
// Print: j' X' m' shift(pos'-w) minoff(min head pos - w) steps   or HALT/OVF
#include <stdio.h>
#include <stdlib.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB0RE_1LC0RA_0LD0LB_1RE0LB_1RF---_0RB0RC";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long j0=atol(v[1]);int X0=atoi(v[2]);long m0=atol(v[3]);int L=c>4?atoi(v[4]):3000;
int w=W/4;for(int i=w-L;i<w;i++)t[i]=1;int x=w+1;for(long i=0;i<j0;i++){t[x]=1;t[x+1]=0;x+=2;}
t[x++]=X0;t[x++]=1;t[x++]=0;t[x++]=0;for(long i=0;i<m0;i++){t[x]=1;t[x+1]=0;x+=2;}t[x++]=1;
int p=w,q=4,hi=x,minp=p;long long last=0;
for(long long st=1;st<4e11;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld minoff %d\n",st,minp-w);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p;if(p<minp)minp=p;
 if(q==4&&t[p]==0&&t[p-1]==1){int y=p+1,j=0;while(t[y]==1&&t[y+1]==0){j++;y+=2;}
   if(j>=1&&t[y+1]==1&&t[y+2]==0&&t[y+3]==0){int X=t[y];int y2=y+4;long mm=0;while(t[y2]==1&&t[y2+1]==0){mm++;y2+=2;}
     if(mm>=1&&t[y2]==0&&t[y2+1]==0&&y2>=hi){ if(st-last!=4){printf("%d %d %ld %d %d %lld\n",j,X,mm-1,p-w,minp-w,st);return 0;} last=st;}}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
}
