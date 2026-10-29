// record events (new cell at either end) of a TM run from start state Q: side state width step interior-hash ends
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; int q=v[2][0]-'A'; long long n=atoll(v[3]); int E=8;
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=200000000; unsigned char*t=calloc(SZ,1); long p=SZ/2,lo=p,hi=p;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b];
   int ev=0; if(p<lo){lo=p;ev=1;} if(p>hi){hi=p;ev=2;}
   if(ev && hi-lo>40){ uint64_t h=1469598103934665603ULL; for(long i=lo+E;i<=hi-E;i++){ h^=t[i]; h*=1099511628211ULL; }
     printf("%c %c %ld %lld %016llx ",ev==1?'L':'R','A'+q,hi-lo+1,s+1,(unsigned long long)h);
     for(long i=lo;i<lo+E;i++) putchar('0'+t[i]); putchar(' '); for(long i=hi-E+1;i<=hi;i++) putchar('0'+t[i]); putchar('\n'); } }
}
