#include <stdio.h>
#include <stdlib.h>
#define W (1<<22)
static unsigned char t[W];
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long N=atol(v[2]);int p=W/2,q=0,lo=p,hi=p;
for(long st=0;st<N;st++){
 if(q==4&&t[p]==1){ // E reading 1 -> next state F at p+1
   printf("step %ld E1 at pos %d (tape %d..%d, head at %d from left, %d from right): ",st,p-W/2,lo-W/2,hi-W/2,p-lo,hi-p);
   for(int k=p-8;k<=p+8;k++)printf(k==p?"[%d]":"%d",t[k]);printf("\n");}
 int b=t[p];if(tq[q][b]<0){printf("halt %ld\n",st);return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p<lo)lo=p;if(p>hi)hi=p;}
printf("width %d\n",hi-lo+1);}
