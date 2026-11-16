// Left-edge events: print state and the block structure (lengths of maximal 1-runs and 0-runs) of the tape,
// only when the structure is not "first 1-block shorter by 2 than at the previous event".
#include <stdio.h>
#include <stdlib.h>
#define W (1<<24)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[2]);int p=W/2,q=0,lo=p,hi=p;long prevfirst=-10;int prevnb=-1;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT at step %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p;
 if(p<lo){lo=p; // structure
   long runs[64];int nr=0;int x=p;while(x<=hi&&nr<64){int v0=t[x];long L=0;while(x<=hi&&t[x]==v0){L++;x++;}runs[nr++]=v0?L:-L;}
   int nb=0;long first=-1;for(int i=0;i<nr;i++)if(runs[i]>0){nb++;if(first<0)first=runs[i];}
   if(!(nb==prevnb&&first==prevfirst-2)){printf("%lld %c:",st,'A'+q);for(int i=0;i<nr;i++)printf(" %ld",runs[i]);printf("\n");}
   prevnb=nb;prevfirst=first;}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
}
