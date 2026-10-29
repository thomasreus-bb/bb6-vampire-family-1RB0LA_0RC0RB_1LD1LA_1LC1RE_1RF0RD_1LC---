#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
const char*M="1RB0LE_1RC---_1RD1RE_1LA0RF_0RC0LA_0LC0RB";
int W[6][2],D[6][2],N[6][2];
void rle(unsigned char*t,long a,long z,int lim){ int out=0;
  long x=a; while(x<=z && out<lim){ int best=1; long bc=1; for(int q=1;q<=4;q++){ long c=1; while(x+(c+1)*q-1<=z && !memcmp(t+x,t+x+c*q,q)) c++; if(c*q>bc*best && c>=3){bc=c;best=q;} }
    if(bc>=3){ out+=printf("("); for(int i=0;i<best;i++) putchar('0'+t[x+i]); out+=best+printf(")^%ld ",bc); x+=bc*best;} else {putchar('0'+t[x]); x++; out++;} }
  if(x<=z) printf("...");
}
int main(int argc,char**argv){ long long maxs=atoll(argv[1]); int lim=atoi(argv[2]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long L=1L<<31; unsigned char*t=calloc(L,1); long h=L/2,lo=h,hi=h; int s=0;
 static const unsigned char unit[14]={1,0,0,0,0,0,1,0,0,0,0,0,0,0}; int prevhas=0;
 for(long long n=0;n<maxs;n++){ int b=t[h]; if(N[s][b]<0){printf("HALT %lld\n",n);return 0;} t[h]=W[s][b]; h+=D[s][b]; s=N[s][b];
   if(h>hi) hi=h;
   if(h<lo){ lo=h; if(s==0 && hi-lo>30){ int has = memmem(t+lo,hi-lo+1,unit,14)!=NULL; if(has!=prevhas){ printf("%c %lld w%ld: ",has?'B':'E',n,hi-lo+1); rle(t,lo,hi,lim); puts(""); fflush(stdout);} prevhas=has; } }
 }
}
