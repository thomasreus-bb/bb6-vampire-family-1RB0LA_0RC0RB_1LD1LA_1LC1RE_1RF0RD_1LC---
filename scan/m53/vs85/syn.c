// argv: table tape(0/1 string, head on the cell left of it, state E) maxsteps. Run to the next E on 0 with blank to the left; print tape after the head.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W (1<<23)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
int p=W/2;int L=strlen(v[2]);for(int i=0;i<L;i++)t[p+1+i]=v[2][i]-'0';long long MX=atoll(v[3]);
int lo=p,hi=p+L,q=4;
for(long long st=1;st<=MX;st++){int r=t[p];if(tq[q][r]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][r];p+=td[q][r];q=tq[q][r];if(p<lo)lo=p;if(p>hi)hi=p;
 if(q==4&&t[p]==0){int ok=1;for(int y=lo;y<p;y++)if(t[y]){ok=0;break;}
  if(ok){int z=hi;while(z>p&&t[z]==0)z--;printf("%lld ",st);for(int y=p+1;y<=z;y++)putchar('0'+t[y]);putchar('\n');return 0;}}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}
printf("MAX\n");}
