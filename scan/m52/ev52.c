// ev52 STEPS : direct simulation of no. 52; at left records in state E whose tape starts with 010 (100)^z, z>=3,
// print step, z and the tape width behind the block (level-chain starts)
#include <stdio.h>
#include <stdlib.h>
int W[8][2],D[8][2],N[8][2];
const char*M="1RB0LC_1RC1RF_1LD0RA_1LE0LD_1RC0LA_0LA---";
int main(int c,char**v){ double n=atof(v[1]); int q=0;
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<27; unsigned char*t=calloc(SZ,1); long p=SZ*3/4,lo=p,hi=p;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s+1);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b];
  if(p>hi)hi=p;
  if(p<lo){ lo=p; if(q==4 && t[lo]==0&&t[lo+1]==1&&t[lo+2]==0){ long i=lo+3,z=0; while(i+2<=hi&&t[i]==1&&t[i+1]==0&&t[i+2]==0){z++;i+=3;}
     if(z>=3){ printf("%lld z=%ld behind=%ld\n",s+1,z,hi-i+1); fflush(stdout);} } } }
 printf("END width=%ld\n",hi-lo+1); }
