#include <stdio.h>
#include <stdlib.h>
static const char*M="1RB0LF_1LC1RA_0RE0RD_---1LE_1LF1RC_1LC1LA";
int W[6][2],D[6][2],N[6][2];
#define SZ 200000000
unsigned char *tp;
int main(int c,char**v){ long long NS=atoll(v[1]); tp=calloc(SZ,1);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long p=SZ/2,lo=p,hi=p; int q=0; long long st=0;
 while(st<NS){ int b=tp[p]; if(N[q][b]<0){printf("HALT %lld\n",st);return 0;} tp[p]=W[q][b]; p+=D[q][b]; q=N[q][b]; st++;
  if(p>hi) hi=p;
  if(p<lo){ lo=p; if(q==2){
     long i=lo; long m=0; while(i+1<=hi&&tp[i]==0&&tp[i+1]==1){m++;i+=2;} long r=0; while(i<=hi&&tp[i]==1){r++;i++;}
     long rest=0; for(long j=i;j<=hi;j++) rest+=tp[j];
     printf("%lld %ld m=%ld r=%ld rest_ones=%ld\n",st,hi-lo+1,m,r,rest); fflush(stdout);} } }
 printf("END %lld\n",st);
}
