// bsim M STATE TAPE MAXSTEPS STOPSTATE : head on the blank cell left of TAPE, run until HALT, a new left record in STOPSTATE, or MAXSTEPS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; int q=v[2][0]-'A'; const char*T=v[3]; long long n=atoll(v[4]); int ss=v[5][0]-'A';
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<27; unsigned char*t=calloc(SZ,1); long p=SZ/2; long L=strlen(T); for(long i=0;i<L;i++) t[p+1+i]=T[i]-'0';
 long lo=p;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld %c\n",s+1,'A'+q);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b];
  if(p<=0||p>=SZ-1){printf("EDGE %lld\n",s);return 0;}
  if(p<lo){lo=p; if(q==ss){ printf("REC %lld ",s+1); long hi=SZ-1; while(hi>p&&!t[hi])hi--; for(long i=p+1;i<=hi && i<p+1+200;i++) putchar('0'+t[i]); printf("\n"); return 0;}} }
 printf("MAX\n"); }
