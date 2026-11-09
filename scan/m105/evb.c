// ev M STATE MAXSTEPS: from the blank tape, print every config where the head is left of all nonzero cells in STATE
// (only when the previous such event was more than 0 steps ago); prints step and the tape right of the head (up to 400 cells)
#include <stdio.h>
#include <stdlib.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; int qs=v[2][0]-'A'; long long n=atoll(v[3]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<26; unsigned char*t=calloc(SZ,1); long p=SZ/2,lo=p,hi=p; int q=0; long first=p; // first = leftmost nonzero
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s+1);return 0;} t[p]=W[q][b]; if(W[q][b]&&p<first) first=p;
  p+=D[q][b]; q=N[q][b]; if(p<lo)lo=p; if(p>hi)hi=p;
  if(q==qs && p<first){ while(first<=hi && !t[first]) first++;
    if(p<first){ printf("%lld ",s+1); long h=hi; while(h>p&&!t[h])h--; for(long i=p+1;i<=h&&i<p+1+200000;i++) putchar('0'+t[i]); if(h>=p+200001) printf("+%ld",h-p-200000); putchar('\n'); } } }
}
