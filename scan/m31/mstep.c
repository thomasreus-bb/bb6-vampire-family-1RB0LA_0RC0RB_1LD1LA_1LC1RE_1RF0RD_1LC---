// one macro step of 1RB1RF_1RC0LD_1LB1RA_1RE1LE_0RC0LB_0RB---:
// from a clean snapshot (blocks b1..bk separated by single 0s, head in state A on the 0 with h blocks to its left)
// to the next clean snapshot.  usage: mstep MAXSTEPS h b1 ... bk     output: OK steps h' | b1' ... | or HALT steps | or TIMEOUT
#include <stdio.h>
#include <stdlib.h>
static const char*M="1RB1RF_1RC0LD_1LB1RA_1RE1LE_0RC0LB_0RB---";
int W[6][2],D[6][2],N[6][2];
static unsigned char*tp; static long lo,hi,zz=0;
static int pz(long k){ return k>=lo&&k+1<=hi&&tp[k]==0&&tp[k+1]==0; }
int main(int c,char**v){ long long MX=atoll(v[1]); int h=atoi(v[2]); int k=c-3; long tot=0; for(int i=3;i<c;i++) tot+=atol(v[i])+1;
 long SZ=2*tot+20000; tp=calloc(SZ,1);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long base=10000, p=base, head=-1; long pos=base;
 if(h==0) head=base-1;
 for(int i=0;i<k;i++){ long n=atol(v[3+i]); for(long j=0;j<n;j++) tp[pos++]=1; if(i==h-1) head=pos; pos++; }
 lo=base-1; hi=pos; if(head<lo) lo=head; if(head>hi) hi=head;
 for(long j=lo;j<hi;j++) zz+=pz(j);
 p=head; int q=0; long long st=0;
 while(st<MX){ int b=tp[p];
  if(st>0&&q==0&&b==0){
    long a=lo; while(a<=hi&&tp[a]==0) a++; long e=hi; while(e>=a&&tp[e]==0) e--;
    long lead= a-lo>=2? a-lo-1:0; long trail= hi-e>=2? hi-e-1:0;
    if(a<=e && zz-lead-trail==0 && p>=a-1 && p<=e+1){
      int hh=0; for(long j=a;j<p;j++) if(tp[j]==0) hh++; if(p>=a) hh++; if(p==a-1) hh=0;
      printf("OK %lld %d |",st,hh); long cur=0; for(long j=a;j<=e;j++){ if(tp[j]) cur++; else { printf(" %ld",cur); cur=0; } } printf(" %ld\n",cur); return 0; } }
  if(N[q][b]<0){ printf("HALT %lld\n",st); return 0; }
  int w=W[q][b]; if(w!=b){ zz-=pz(p-1)+pz(p); tp[p]=w; zz+=pz(p-1)+pz(p); }
  p+=D[q][b]; q=N[q][b]; st++;
  if(p<1||p>=SZ-1){ printf("EDGE\n"); return 0; }
  if(p<lo){ lo=p; zz+=pz(lo); } if(p>hi){ hi=p; zz+=pz(hi-1); } }
 printf("TIMEOUT\n"); }
