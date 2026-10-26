// fast clean snapshots (state A reading 0, tape = 1-blocks separated by single 0s)
#include <stdio.h>
#include <stdlib.h>
static const char*M="1RB1RF_1RC0LD_1LB1RA_1RE1LE_0RC0LB_0RB---";
int W[6][2],D[6][2],N[6][2];
#define SZ 8000000
unsigned char tp[SZ];
static long lo,hi; static long zz=0;
static int pz(long k){ return k>=lo&&k+1<=hi&&tp[k]==0&&tp[k+1]==0; }
int main(int c,char**v){ long long NS=atoll(v[1]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long p=SZ/2; lo=hi=p; int q=0; long long st=0;
 while(st<NS){ int b=tp[p];
  if(q==0&&b==0){
    long a=lo; while(a<=hi&&tp[a]==0) a++; long e=hi; while(e>=a&&tp[e]==0) e--;
    long lead= a-lo>=2? a-lo-1:0; long trail= hi-e>=2? hi-e-1:0;
    if(a<=e && zz-lead-trail==0 && p>=a-1){
      printf("%lld |",st); int h=-1,nr=0; long cur=0;
      for(long k=a;k<=e;k++){ if(tp[k]) cur++; else { if(k==p) h=nr; printf(" %ld",cur); cur=0; nr++; } }
      printf(" %ld h%d\n",cur, p>e? nr+1 : h); } }
  if(N[q][b]<0){printf("HALT %lld\n",st);return 0;}
  int w=W[q][b];
  if(w!=b){ zz-=pz(p-1)+pz(p); tp[p]=w; zz+=pz(p-1)+pz(p); }
  p+=D[q][b]; q=N[q][b]; st++;
  if(p<lo){ lo=p; zz+=pz(lo); }
  if(p>hi){ hi=p; zz+=pz(hi-1); } }
}
