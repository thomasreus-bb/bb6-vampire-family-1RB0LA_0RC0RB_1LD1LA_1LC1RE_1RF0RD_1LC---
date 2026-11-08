// f30 N1 N2 : for n in [N1,N2] build tape 1^n 0 0 (head on the last 0, state D, a right record),
// run until HALT or the next right record in state D whose tape is a single block 1^m 0 0; print n m steps
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int W[8][2],D[8][2],N[8][2];
const char*M="1RB0LE_1LB1RC_0RF0RD_1RE0LA_1LA1RE_---0RB";
int main(int c,char**v){ long n1=atol(v[1]),n2=atol(v[2]); double lim=c>3?atof(v[3]):1e10;
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<26; unsigned char*t=malloc(SZ);
 for(long n=n1;n<=n2;n++){ memset(t,0,SZ); long lo=SZ/8,k=lo; for(long j=0;j<n;j++)t[k++]=1; t[k++]=0; t[k]=0; long p=k,hi=k; int q=3; int done=0;
  for(long long s=0;s<lim;s++){ int b=t[p]; if(N[q][b]<0){printf("%ld HALT %lld\n",n,s+1);done=1;break;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b]; if(p<lo)lo=p;
   if(p>hi){ hi=p; if(q==3){ long i=lo; while(!t[i])i++; long a=i; while(t[i])i++; if(i==hi-1 && i-a!=n){ printf("%ld %ld %lld\n",n,i-a,s+1); done=1; break; } } } }
  if(!done)printf("%ld MAX\n",n); fflush(stdout); }
}
