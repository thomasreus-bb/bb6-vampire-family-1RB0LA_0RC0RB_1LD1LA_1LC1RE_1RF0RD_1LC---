/* batch version of cyc83: each input line "N r S maxsteps" -> one output line (BELL M r' S' steps | HALT s | MAX | TAPE) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
const char*TM="1LB1LA_1RC0LB_1RD0RB_1LA0RE_---1RF_1RB0RA";
int W[8][2],D[8][2],NX[8][2];
static char S[1<<20];
int main(){
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=TM+7*i+3*b; if(x[0]=='-'){NX[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;NX[i][b]=x[2]-'A';}
 long cap=0; unsigned char*t=NULL; long N; int r; long long mx;
 while(scanf("%ld %d %s %lld",&N,&r,S,&mx)==4){
  const char*s0=strcmp(S,"-")?S:"";
  long L=1+N+r+strlen(s0); long SZ=8*L+(1<<20);
  if(SZ>cap){ free(t); t=malloc(SZ); cap=SZ; }
  memset(t,0,SZ); long base=SZ/2;
  for(long i=0;i<N;i++) t[base+1+i]=1; for(long i=0;s0[i];i++) t[base+1+N+r+i]=s0[i]-'0';
  long p=base, lo=base, hi=base+L-1; int q=1; long long s=0; int done=0;
  for(;s<mx;s++){ int b=t[p]; if(NX[q][b]<0){printf("HALT %lld\n",s);done=1;break;} t[p]=W[q][b]; p+=D[q][b]; q=NX[q][b];
   if(p>hi)hi=p;
   if(p<lo){ lo=p; if(q==1 && t[p]==0){ long i=p+1; while(i<=hi&&t[i]) i++; long M=i-p-1; long j=i; while(j<=hi&&!t[j]) j++; long rr=j-i;
       if(M>N && rr>=1 && rr<=3 && j<=hi){ printf("BELL %ld %ld ",M,rr); long e=hi; while(e>=j&&!t[e]) e--; for(long k=j;k<=e;k++) putchar('0'+t[k]); printf(" %lld\n",s+1); done=1; break;} } }
   if(p<2||p>SZ-3){printf("TAPE\n");done=1;break;} }
  if(!done) printf("MAX\n");
  fflush(stdout);
 }
}
