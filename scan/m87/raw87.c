// no. 87: print raw tape (from head) at left-edge events of state A, and right-edge events of state E
#include <stdio.h>
#include <stdlib.h>
#define W (1<<26)
static unsigned char t[W];
int main(int c,char**v){const char*s="1RB1LC_1RC0RF_1RD0LB_1RE0LD_1LF---_0RA1LA";int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[1]);int p=W/2,q=0,lo=p,hi=p;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT %lld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];
 int ev=0; if(p<lo){lo=p;if(q==0)ev=1;} if(p>hi){hi=p;if(q==4)ev=2;}
 if(ev){printf("%c %lld ",ev==1?'L':'R',st+1);for(int y=lo;y<=hi;y++)putchar(y==p?'*':'0'+t[y]);putchar('\n');}
 if(p<2||p>W-3){printf("OVF\n");return 0;}}}
