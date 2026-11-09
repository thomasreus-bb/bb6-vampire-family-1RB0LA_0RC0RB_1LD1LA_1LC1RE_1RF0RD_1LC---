#include <stdio.h>
#include <stdlib.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; long long n=atoll(v[2]); int q=0; long cnt[2][6]={{0}};
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=400000000; unsigned char*t=calloc(SZ,1); long p=SZ/2,lo=p,hi=p;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s+1);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b];
  if(p<lo){lo=p;cnt[0][q]++;} if(p>hi){hi=p;cnt[1][q]++;} }
 for(int sd=0;sd<2;sd++){printf("%c:",sd?'R':'L');for(int i=0;i<6;i++)printf(" %c=%ld",'A'+i,cnt[sd][i]);printf("\n");} printf("width %ld left %ld right %ld\n",hi-lo,SZ/2-lo,hi-SZ/2);}
