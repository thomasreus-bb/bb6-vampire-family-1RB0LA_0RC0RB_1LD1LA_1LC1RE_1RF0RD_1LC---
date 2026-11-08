// z52 Z1 Z2 : for z in [Z1,Z2] build tape "010 (100)^z 1", head on the first cell in state E,
// run until HALT or until an L-E record of the form (010)^x 01 ; print z and outcome
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int W[8][2],D[8][2],N[8][2];
const char*M="1RB0LC_1RC1RF_1LD0RA_1LE0LD_1RC0LA_0LA---";
int main(int c,char**v){ long z1=atol(v[1]),z2=atol(v[2]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1<<26; unsigned char*t=malloc(SZ);
 for(long z=z1;z<=z2;z++){ memset(t,0,SZ); long p=SZ/4,lo=p; long k=p; t[k++]=0;t[k++]=1;t[k++]=0; for(long j=0;j<z;j++){t[k++]=1;t[k++]=0;t[k++]=0;} t[k++]=1; long hi=k-1; int q=4;
  long long s=0, lim=400LL*z*z+100000; int done=0;
  for(;s<lim;s++){ int b=t[p]; if(N[q][b]<0){printf("%ld HALT %lld\n",z,s+1);done=1;break;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b]; if(p>hi)hi=p;
   if(p<lo){ lo=p; if(q==4){ long w=hi-lo+1; if(w%3==2 && t[hi]==1 && t[hi-1]==0){ int ok=1; for(long i=lo;i<hi-1;i+=3) if(t[i]||!t[i+1]||t[i+2]){ok=0;break;} if(ok){printf("%ld X %ld %lld\n",z,(w-2)/3,s+1);done=1;break;} } } } }
  if(!done) printf("%ld MAX\n",z); fflush(stdout); }
}
