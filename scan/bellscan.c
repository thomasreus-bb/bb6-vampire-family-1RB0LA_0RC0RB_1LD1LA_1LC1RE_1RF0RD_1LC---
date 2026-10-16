// Bell scan v3 (two-block sweeps).
// At every head reversal the tape is run-length compressed into blocks w^n (|w|<=3).
// Of the long blocks (n>=4) we take the leftmost and the rightmost (they must differ).
// Per turn type (R->L, L->R) we look for "sweeps": >=MINRUN consecutive reversals in which one long
// block shrinks by a constant d>=1 and the other grows by a constant e>=1 (words fixed).
// The start count of the shrinking block in each sweep phase ("Bell start") is recorded.
// A Bell machine (TM1/TM2 type) shows many sweep phases whose start counts grow geometrically.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define NT (1<<23)
#define MINRUN 4
static unsigned char t[NT];
typedef struct { int wl,wr; long nl,nr; int ok; } Rv;   // w encoded as (len<<4)|bits
static Rv rv[24][300000]; static int nrv[24];
static int enc(long x,int p){ int best=1<<30; for(int r=0;r<p;r++){ int v=0; for(int i=0;i<p;i++) v=v*2+t[x+(r+i)%p]; if(v<best) best=v; } return (p<<4)|best; }
static int allzero(long x,int p){ for(int i=0;i<p;i++) if(t[x+i]) return 0; return 1; }
int main(int argc,char**argv){
  const char*tm=argv[1]; long long maxs=atoll(argv[2]); long long budget=atoll(argv[3]);
  int W[6][2],M[6][2],X[6][2];
  for(int s=0;s<6;s++)for(int b=0;b<2;b++){const char*p=tm+s*7+b*3;
    if(p[0]=='-'){X[s][b]=-1;W[s][b]=1;M[s][b]=1;continue;} W[s][b]=p[0]-'0';M[s][b]=p[1]=='R'?1:-1;X[s][b]=p[2]-'A';}
  memset(t,0,NT); long h=NT/2,lo=h,hi=h; int st=0,lastm=0; memset(nrv,0,sizeof nrv); long long work=0;
  long long i; const char*end="LIMIT";
  for(i=0;i<maxs;i++){
    int b=t[h],n=X[st][b]; if(n<0){end="HALT";break;}
    int m=M[st][b]; t[h]=W[st][b];
    if(lastm && m!=lastm && work<budget){
      int tt=(m>0)*12+st*2+b; long a=lo,z=hi; while(a<z&&t[a]==0)a++; while(z>a&&t[z]==0)z--;
      work+=z-a+1;
      Rv r={0,0,0,0,0}; int found=0; long x=a;
      while(x<=z){
        int bp=1; long bc=1;
        for(int p=1;p<=3;p++){ long c=1; while(x+(c+1)*p-1<=z && !memcmp(t+x,t+x+c*p,p)) c++; if(c>=4 && c*p>bc*bp){bp=p;bc=c;} }
        if(bc>=4 && !allzero(x,bp)){ int w=enc(x,bp); if(!found){r.wl=w;r.nl=bc;found=1;} r.wr=w; r.nr=bc; found++; x+=bc*bp; }
        else if(bc>=4) x+=bc*bp; else x++;
      }
      if(found>=3){ r.ok=1; if(nrv[tt]<300000) rv[tt][nrv[tt]++]=r; }
      else if(nrv[tt]<300000){ r.ok=0; rv[tt][nrv[tt]++]=r; }
    }
    lastm=m; h+=m; st=n; if(h<lo)lo=h; if(h>hi)hi=h;
    if(h<2||h>NT-3){end="OVF";break;}
  }
  long starts[200000]; int ns=0;
  for(int tt=0;tt<24;tt++){ Rv*q=rv[tt]; int N=nrv[tt]; int j=0;
    while(j+1<N){
      int k=j;
      if(q[j].ok&&q[j+1].ok&&q[j].wl==q[j+1].wl&&q[j].wr==q[j+1].wr){
        long dl=q[j+1].nl-q[j].nl, dr=q[j+1].nr-q[j].nr;
        if((dl<0&&dr>0)||(dl>0&&dr<0)){
          while(k+1<N&&q[k+1].ok&&q[k+1].wl==q[j].wl&&q[k+1].wr==q[j].wr&&q[k+1].nl-q[k].nl==dl&&q[k+1].nr-q[k].nr==dr) k++;
        }
        if(k-j>=MINRUN){ long s0= dl<0? q[j].nl : q[j].nr; if(ns<200000) starts[ns++]=s0; j=k+1; continue; }
      }
      j++;
    }
  }
  // records of starts (order mixes the two turn types; use sorted unique growth of records)
  // sort starts and count distinct "levels" that are geometric: take records after sorting by value
  long mx=0; int nrec=0; long rec[2000];
  // to get temporal order merge is lost; approximate with sorted values clustered by 5%
  for(int a=0;a<ns;a++) for(int b2=a+1;b2<ns;b2++) if(starts[b2]<starts[a]){long tmp=starts[a];starts[a]=starts[b2];starts[b2]=tmp;}
  for(int a=0;a<ns;a++){ if(starts[a]>mx*1.05+1){ if(nrec<2000) rec[nrec++]=starts[a]; } if(starts[a]>mx) mx=starts[a]; }
  double lr=0,l2=0; int c=0; for(int a=1;a<nrec;a++){ double q=log((double)rec[a]/rec[a-1]); lr+=q; l2+=q*q; c++; } double sd=c>1?sqrt(fabs(l2/c-(lr/c)*(lr/c))):0;
  printf("%s end=%s steps=%lld phases=%d levels=%d max=%ld ratio=%.3f sd=%.3f :",tm,end,i,ns,nrec,mx,c?exp(lr/c):0,sd);
  int from=nrec>14?nrec-14:0; for(int a=from;a<nrec;a++) printf(" %ld",rec[a]); printf("\n");
}
