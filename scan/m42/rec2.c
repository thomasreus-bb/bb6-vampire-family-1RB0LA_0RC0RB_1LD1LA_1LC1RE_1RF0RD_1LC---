// rec2 TM MAXSTEPS MODE: simulate from blank. At each new leftmost cell print step, state, tape as a string (cells lo..hi).
// MODE 0: all records; MODE n>0: only records where the head state is A... (print all, filter in python)
#include <stdio.h>
#include <stdlib.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; long long n=atoll(v[2]); int q=0; long maxw=atol(v[3]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<28; unsigned char*t=calloc(SZ,1); long p=SZ/2, lo=p, hi=p;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld %c\n",s,'A'+q);return 0;}
  t[p]=W[q][b]; p+=D[q][b]; q=N[q][b];
  if(p>hi){hi=p;}
  if(p<lo){ lo=p; printf("%lld %c ",s,'A'+q); if(hi-lo<maxw){for(long i=lo;i<=hi;i++)putchar('0'+t[i]);} else printf("W%ld",hi-lo+1); putchar('\n'); }
 }
 printf("END\n");
}
