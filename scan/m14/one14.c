// from tape (01)^m 1^r with the head on the new cell left of it in state C, run to the next new left cell in state C
#include <stdio.h>
#include <stdlib.h>
static const char*M="1RB0LF_1LC1RA_0RE0RD_---1LE_1LF1RC_1LC1LA";
int W[6][2],D[6][2],N[6][2];
int main(int c,char**v){ long m=atol(v[1]), r=atol(v[2]); long SZ=4*(2*m+r)+100000; unsigned char*tp=calloc(SZ,1);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long base=SZ/2, p=base; for(long i=0;i<m;i++){tp[p++]=0;tp[p++]=1;} for(long i=0;i<r;i++) tp[p++]=1;
 long lo=base, hi=p-1; p=base; int q=2; long long st=0;
 // note: the head cell (base-1) is the new left cell; tape starts at base with 0 1 ...
 while(st<4000000000LL){ int b=tp[p]; if(N[q][b]<0){ printf("HALT %lld\n",st); return 0;} tp[p]=W[q][b]; p+=D[q][b]; q=N[q][b]; st++;
  if(p>hi) hi=p;
  if(p<lo){ lo=p; if(q==2){ long i=lo; long mm=0; while(i+1<=hi&&tp[i]==0&&tp[i+1]==1){mm++;i+=2;} long rr=0; while(i<=hi&&tp[i]==1){rr++;i++;} long rest=0; for(long j=i;j<=hi;j++) rest+=tp[j];
      printf("OK %lld %ld %ld %ld\n",st,mm,rr,rest); return 0; } } }
 printf("TIMEOUT\n"); }
