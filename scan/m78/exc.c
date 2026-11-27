/* exc TM N : for each right record, print step, state, hi-lo, and depth = hi - (min head pos since previous right record) */
#include <stdio.h>
#include <stdlib.h>
int W[8][2],D[8][2],NX[8][2];
int main(int c,char**v){ const char*M=v[1]; long long n=atoll(v[2]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){NX[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;NX[i][b]=x[2]-'A';}
 long SZ=1<<26; unsigned char*t=calloc(SZ,1); long p=SZ/2,lo=p,hi=p,mn=p; int q=0;
 for(long long s=0;s<n;s++){ int b=t[p]; if(NX[q][b]<0){printf("HALT %lld\n",s);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=NX[q][b];
  if(p<mn)mn=p; if(p<lo){lo=p; printf("L %lld %c %ld\n",s+1,'A'+q,hi-lo);}
  if(p>hi){hi=p; printf("R %lld %c %ld %ld\n",s+1,'A'+q,hi-lo,hi-mn); mn=p;} }
}
