#include <stdio.h>
#include <stdlib.h>
#define W (1<<20)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long N=atol(v[2]);int a=atoi(v[3])+W/2,z=atoi(v[4])+W/2;int p=W/2,q=0;
for(long st=0;st<N;st++){int b=t[p];t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];}
printf("state %c head %d\n",'A'+q,p-W/2);for(int x=a;x<=z;x++){if(x==p)putchar('[');putchar('0'+t[x]);if(x==p)putchar(']');}putchar('\n');}
