// run no. 25 from the blank tape until the first P config: left part exactly "10" (then blanks), A on 0, a 1 to its right
#include <stdio.h>
#include <stdlib.h>
int W[8][2],D[8][2],N[8][2];
int main(){ const char*M="1RB0LE_1LC0RD_0RA1LD_0LC1RA_1LF1LA_---1LA";
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<27; unsigned char*t=calloc(SZ,1); long p=SZ/2,lo=p,hi=p; int q=0; int cnt=0;
 for(long long s=0;s<20000000000LL;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT\n");return 0;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b]; if(p<lo)lo=p; if(p>hi)hi=p;
  if(q==0&&t[p]==0&&t[p-1]==0&&t[p-2]==1&&t[p+1]==1){int ok=1; for(long i=lo;i<p-2;i++) if(t[i]){ok=0;break;}
   if(ok){ printf("P %lld ",s+1); long h=hi; while(h>p&&!t[h])h--; for(long i=p+1;i<=h;i++) putchar('0'+t[i]); printf("\n"); if(++cnt>=40) return 0;}}}
}
