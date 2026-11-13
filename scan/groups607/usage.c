// usage N: reads machine codes from stdin; runs each from the blank tape for N steps and prints
// the code, the steps done, and how often each of the 12 transitions A0 A1 ... F1 was used.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc,char**argv){ long long N=atoll(argv[1]); char M[64]; long SZ=1L<<26; unsigned char*t=calloc(SZ,1);
 while(scanf("%63s",M)==1){ int W[6][2],D[6][2],X[6][2];
  for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){X[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;X[i][b]=x[2]-'A';}
  memset(t,0,SZ); long p=SZ/2; int q=0; long long c[6][2]={{0}}, last[6][2]={{0}}; long long s; const char*why="max";
  for(s=0;s<N;s++){ int b=t[p]; if(X[q][b]<0){why="halt";break;} c[q][b]++; last[q][b]=s; t[p]=W[q][b]; p+=D[q][b]; q=X[q][b]; if(p<1||p>=SZ-1){why="edge";break;} }
  printf("%s %lld %s",M,s,why); for(int i=0;i<6;i++)for(int b=0;b<2;b++) printf(" %lld",c[i][b]); printf(" |"); for(int i=0;i<6;i++)for(int b=0;b<2;b++) printf(" %lld",last[i][b]); printf("\n"); fflush(stdout); }
}
