/* cyc83 N r S maxsteps : start mirrored TM83 in state B at cell 0 of tape 0 1^N 0^r S.
   run until a left record in state B whose tape is 0 1^M 0^r' 1... with r' in 1..3 and M > N.
   print: BELL M r' S' steps   |  HALT steps  | MAX */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
const char*TM="1LB1LA_1RC0LB_1RD0RB_1LA0RE_---1RF_1RB0RA";
int W[8][2],D[8][2],NX[8][2];
int main(int c,char**v){ long N=atol(v[1]); int r=atoi(v[2]); const char*S=strcmp(v[3],"-")?v[3]:""; long long mx=atoll(v[4]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=TM+7*i+3*b; if(x[0]=='-'){NX[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;NX[i][b]=x[2]-'A';}
 long L=1+N+r+strlen(S); long SZ=8*L+(1<<22); unsigned char*t=calloc(SZ,1); long base=SZ/2;
 for(long i=0;i<N;i++) t[base+1+i]=1; for(long i=0;S[i];i++) t[base+1+N+r+i]=S[i]-'0';
 long p=base, lo=base, hi=base+L-1; int q=1; long long s=0;
 for(;s<mx;s++){ int b=t[p]; if(NX[q][b]<0){printf("HALT %lld\n",s);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=NX[q][b];
   if(p>hi)hi=p;
   if(p<lo){ lo=p; if(q==1 && t[p]==0){ long i=p+1; while(i<=hi&&t[i]) i++; long M=i-p-1; long j=i; while(j<=hi&&!t[j]) j++; long rr=j-i;
       if(M>N && rr>=1 && rr<=3 && j<=hi){ printf("BELL %ld %ld ",M,rr); long e=hi; while(e>=j&&!t[e]) e--; for(long k=j;k<=e;k++) putchar('0'+t[k]); printf(" %lld\n",s+1); return 0;} } }
   if(p<2||p>SZ-3){printf("TAPE\n");return 0;} }
 printf("MAX\n"); }
