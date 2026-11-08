// rec M STEPS SIDE STATE : at every new record on SIDE in STATE print step, head offset and full tape as 0/1 string
#include <stdio.h>
#include <stdlib.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; long long n=atoll(v[2]); char side=v[3][0]; int st=v[4][0]-'A'; int q=0;
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=400000000; unsigned char*t=calloc(SZ,1); long p=SZ/2,lo=p,hi=p;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s+1);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b];
  int ev=0; if(p<lo){lo=p;ev='L';} if(p>hi){hi=p;ev='R';}
  if(ev==side && q==st){ printf("%lld %ld ",s+1,p-lo); for(long i=lo;i<=hi;i++) putchar('0'+t[i]); putchar('\n'); } }
 printf("END\n"); }
