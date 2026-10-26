// one Bell of 1RB1RF_1RC0LD_1LB1RA_1RE1LE_0RC0LB_0RB--- from a Bell start tape  b1 0 b2 0 ... bk 0 , head on the new cell right of it, state A
// usage: one MAXSTEPS b1 b2 ... bk      prints: OK steps | runs     or HALT steps | runs      or TIMEOUT
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char*M="1RB1RF_1RC0LD_1LB1RA_1RE1LE_0RC0LB_0RB---";
int W[6][2],D[6][2],N[6][2];
static unsigned char*tp; static long SZ;
static void pr(long lo,long hi){ long i=lo; while(i<=hi&&tp[i]==0) i++; long j=hi; while(j>=i&&tp[j]==0) j--;
  long r=i; while(r<=j){ if(tp[r]==1){ long s=r; while(r<=j&&tp[r]==1) r++; printf(" %ld",r-s); } else { long s=r; while(r<=j&&tp[r]==0) r++; if(r-s>1) printf(" z%ld",r-s); } } printf("\n"); }
int main(int c,char**v){ long long MX=atoll(v[1]); long tot=0; for(int i=2;i<c;i++) tot+=atol(v[i])+1;
 SZ=tot*3+1000; tp=calloc(SZ,1);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long p=200; for(int i=2;i<c;i++){ long n=atol(v[i]); for(long k=0;k<n;k++) tp[p++]=1; if(i<c-1) p++; }
 long lo=200,hi=p-1; int q=0; long long st=0; // head at p (new cell), state A
 hi=p; 
 while(st<MX){ int b=tp[p]; if(N[q][b]<0){ printf("HALT %lld |",st); pr(lo,hi); return 0; }
   tp[p]=W[q][b]; p+=D[q][b]; q=N[q][b]; st++;
   if(p<lo){ lo=p; if(p<2){ printf("LEFTEDGE\n"); return 0;} }
   if(p>hi){ hi=p; if(p>=SZ-2){ printf("RIGHTEDGE\n"); return 0;} if(q==0){ printf("OK %lld |",st); pr(lo,hi-1); return 0; } } }
 printf("TIMEOUT\n"); }
