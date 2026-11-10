// evlev M STATE TAPE MAXSTEPS: from "head on the blank left of TAPE in STATE", print every config where the head is
// left of all nonzero cells (any state), until the next such config in STATE whose tape starts with UNIT=110 twice
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; int qs=v[2][0]-'A'; const char*T=v[3]; long long n=atoll(v[4]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<24; unsigned char*t=calloc(SZ,1); long p=SZ/4; long L=strlen(T); for(long i=0;i<L;i++) t[p+1+i]=T[i]-'0';
 int q=qs; long lo=p,hi=p+L,first=p+1;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s+1);return 0;} t[p]=W[q][b]; if(W[q][b]&&p<first)first=p;
  p+=D[q][b]; q=N[q][b]; if(p<lo)lo=p; if(p>hi)hi=p;
  if(p<first){ while(first<=hi&&!t[first])first++;
   if(p<first){ printf("%lld %c ",s+1,'A'+q); long h=hi; while(h>p&&!t[h])h--; for(long i=p+1;i<=h;i++) putchar('0'+t[i]); putchar('\n');
     if(q==qs && t[p+1]==1&&t[p+2]==1&&t[p+3]==0&&t[p+4]==1&&t[p+5]==1&&t[p+6]==0 && s>10) return 0; } } }
}
