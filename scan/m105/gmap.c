// gmap M STATE PREFIX TAPE MAXSTEPS: head on the blank cell left of TAPE in STATE; run to the next config in STATE with
// the head left of all nonzero cells and the cells right of the head = PREFIX 1^n (n>=1) ...; prints "P steps rest"
// (rest = everything after PREFIX), or HALT / MAX
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; int qs=v[2][0]-'A'; const char*P=v[3]; const char*T=v[4]; long long n=atoll(v[5]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<27; unsigned char*t=calloc(SZ,1); long p=SZ/4; long L=strlen(T), PL=strlen(P);
 for(long i=0;i<L;i++) t[p+1+i]=T[i]-'0';
 int q=qs; long lo=p,hi=p+L, first=p+1; while(first<=hi&&!t[first]) first++;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s+1);return 0;} t[p]=W[q][b]; if(W[q][b]&&p<first) first=p;
  p+=D[q][b]; q=N[q][b]; if(p<lo)lo=p; if(p>hi)hi=p; if(p<=1||p>=SZ-2){printf("EDGE\n");return 0;}
  if(q==qs && p<first){ while(first<=hi && !t[first]) first++;
    if(p<first){ int ok=1; for(long i=0;i<PL;i++) if(t[p+1+i]!=P[i]-'0'){ok=0;break;}
      if(ok && t[p+1+PL]==1){ printf("P %lld ",s+1); long h=hi; while(h>p&&!t[h])h--; for(long i=p+1+PL;i<=h;i++) putchar('0'+t[i]); printf("\n"); return 0; } } } }
 printf("MAX\n"); }
