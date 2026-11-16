// every left-edge event: state and 1-block lengths mod 3 pattern (counts distinct patterns)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W (1<<24)
static unsigned char t[W];
char pats[20000][80];long cnt[20000];int np=0;
int main(int c,char**v){const char*s=v[1];int tw[6][2],td[6][2],tq[6][2];
for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;if(x[0]=='-'){tq[i][b]=-1;continue;}tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
long long N=atoll(v[2]);int p=W/2,q=0,lo=p,hi=p;
for(long long st=0;st<N;st++){int b=t[p];if(tq[q][b]<0){printf("HALT\n");return 0;}
 t[p]=tw[q][b];p+=td[q][b];q=tq[q][b];if(p>hi)hi=p;
 if(p<lo){lo=p; if(st<100000) continue; char k[80];int n=0;k[n++]='A'+q;k[n++]=':';int x=p;
   while(x<=hi&&n<70){int v0=t[x];long L=0;while(x<=hi&&t[x]==v0){L++;x++;}
     if(x>hi&&!v0)break; if(v0){k[n++]=(L>5?'0'+L%6:'a'+L);}else{k[n++]=(L==1?'.':L==2?'_':'#');}}
   k[n]=0;int i;for(i=0;i<np;i++)if(!strcmp(pats[i],k)){cnt[i]++;break;} if(i==np&&np<20000){strcpy(pats[np],k);cnt[np++]=1;}}
 if(p<2||p>W-3)break;}
for(int i=0;i<np;i++)printf("%8ld %s\n",cnt[i],pats[i]);}
