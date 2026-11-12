// bell N MAXSTEPS: no. 41 from the Bell configuration 1 (10)^N [0], state A; reports HALT or the next Bell
#include <stdio.h>
#include <stdlib.h>
const char*M="1RB1LD_1RC0RA_1LA1RE_0LA0LB_0RB1RF_---1RD";
int W[6][2],D[6][2],Nx[6][2];
int main(int c,char**v){ long n=atol(v[1]); long long maxs=atoll(v[2]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){Nx[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;Nx[i][b]=x[2]-'A';}
 long SZ=40*n+100000; unsigned char*t=calloc(SZ,1); long base=SZ/2,p=base; t[p++]=1; for(long i=0;i<n;i++){t[p++]=1;t[p++]=0;} int q=0; long hi=p;
 for(long long s=0;s<maxs;s++){ int b=t[p]; if(Nx[q][b]<0){printf("HALT after %lld steps (state %c reads %d)\n",s,'A'+q,b);return 0;}
  t[p]=W[q][b]; p+=D[q][b]; q=Nx[q][b]; if(p<=1||p>=SZ-2){printf("EDGE\n");return 1;}
  if(p>hi){ hi=p; if(q==0){ // new right record in state A: check Bell form
      long i=p-1,k=0; while(i>=1&&t[i]==0&&t[i-1]==1){k++;i-=2;} if(t[i]==1&&t[i-1]==0&&k>0){ long j=i-1; while(j>0&&j>i-50&&t[j]==0)j--; if(j==i-50){printf("next Bell n = %ld after %lld steps\n",k,s+1);return 0;} } } } }
 printf("no halt in %lld steps\n",maxs); return 0; }
