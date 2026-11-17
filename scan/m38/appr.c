// After step T0, report every turning point (head moved left, then right) at position < w+R, with the window.
#include <stdio.h>
#include <stdlib.h>
#define W (1<<20)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long N=atol(v[2]);int w=atoi(v[3])+W/2;long T0=atol(v[4]);int R=atoi(v[5]);int p=W/2,q=0,lastd=0;int shown=0;
for(long st=0;st<N;st++){int b=t[p];int d=td[q][b];
 if(st>T0&&lastd<0&&d>0&&p<w+R&&shown<60){printf("%9ld %c%d @w%+d: ",st,'A'+q,b,p-w);for(int x=w-2;x<=w+R+4;x++){if(x==p)putchar('[');putchar('0'+t[x]);if(x==p)putchar(']');}putchar('\n');shown++;}
 t[p]=tw[q][b];p+=d;q=tq[q][b];lastd=d;}
}
