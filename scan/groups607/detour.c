// Detours in the real run: simulate M1 from the blank tape (start state Q1) for N steps.
// At every use of slot (q,s) (up to MAXU uses, then every SAMPLE-th), copy the configuration and run
// M1 and M2 (M2 = second table, renamed/mirrored into M1's naming) from it for up to L steps each;
// look for a common configuration (Zobrist hash + full compare). Report k1,k2 and the cells touched.
// usage: ./detour TAB1 TAB2 Q1 slotstate slotsym N L MAXU SAMPLE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define W (1<<22)
typedef struct{int w,d,q;} Tr;
Tr t1[6][2],t2[6][2];
void parse(const char*s,Tr t[6][2]){for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=s+7*i+3*b;
 if(x[0]=='-'){t[i][b].q=-1;continue;} t[i][b].w=x[0]-'0';t[i][b].d=x[1]=='R'?1:-1;t[i][b].q=x[2]-'A';}}
static uint64_t Z[W],ZS[6];
static unsigned char base[W],ta[W],tb[W];
uint64_t rnd(){static uint64_t x=88172645463325252ULL;x^=x<<13;x^=x>>7;x^=x<<17;return x;}
#define HS (1<<22)
static uint64_t hk[HS];static int hv[HS];static int hgen[HS];int gen=0;
int main(int argc,char**argv){
 parse(argv[1],t1);parse(argv[2],t2);int q=argv[3][0]-'A';int sq=argv[4][0]-'A',ss=atoi(argv[5]);
 long N=atol(argv[6]),L=atol(argv[7]),MAXU=atol(argv[8]),SAMPLE=atol(argv[9]);
 for(int i=0;i<W;i++)Z[i]=rnd();for(int i=0;i<6;i++)ZS[i]=rnd();
 int pos=W/2;long uses=0,ok=0,bad=0;long maxk=0;int maxspan=0;long hist[8]={0};
 for(long st=0;st<N;st++){
  int s=base[pos];
  if(q==sq&&s==ss){uses++;
   if(uses<=MAXU||uses%SAMPLE==0){
    // run M1 from copy, store hashes
    memcpy(ta,base,W);int p=pos,qq=q;uint64_t h=0;
    // hash of the difference to base only (both start from base)
    gen++;int lo=pos,hi=pos;long k1=-1,k2=-1;
    for(long k=1;k<=L;k++){int b=ta[p];Tr*t=&t1[qq][b];if(t->q<0){k=L+1;break;}
      if(t->w!=b)h^=Z[p];ta[p]=t->w;p+=t->d;qq=t->q;if(p<lo)lo=p;if(p>hi)hi=p;
      uint64_t key=h^ZS[qq]^(Z[p]*31);unsigned ix=(key*0x9E3779B97F4A7C15ULL)>>42;
      while(hgen[ix]==gen)ix=(ix+1)&(HS-1);hgen[ix]=gen;hk[ix]=key;hv[ix]=(int)k;}
    // run M2, look up (full compare done by re-running M1 to k1 would be costly; hash 64-bit is trusted, collisions ~0)
    memcpy(tb,base,W);p=pos;qq=q;h=0;
    for(long k=1;k<=L&&k1<0;k++){int b=tb[p];Tr*t=&t2[qq][b];if(t->q<0)break;
      if(t->w!=b)h^=Z[p];tb[p]=t->w;p+=t->d;qq=t->q;if(p<lo)lo=p;if(p>hi)hi=p;
      uint64_t key=h^ZS[qq]^(Z[p]*31);unsigned ix=(key*0x9E3779B97F4A7C15ULL)>>42;
      while(hgen[ix]==gen){if(hk[ix]==key){k1=hv[ix];k2=k;break;}ix=(ix+1)&(HS-1);}}
    if(k1>0){ok++;long m=k1>k2?k1:k2;if(m>maxk)maxk=m;int span=hi-lo+1;if(span>maxspan)maxspan=span;
      int b=0;while(b<7&&m>=(10L<<(3*b)))b++;hist[b]++;}
    else{bad++;if(bad<=3)printf("  no meeting within %ld steps at use %ld (step %ld)\n",L,uses,st);}
   }}
  Tr*t=&t1[q][s];if(t->q<0){printf("  M1 halts at step %ld\n",st);break;}
  base[pos]=t->w;pos+=t->d;q=t->q;if(pos<1||pos>=W-1){printf("  tape limit\n");break;}
 }
 printf("uses %ld, tested %ld: meet %ld, no meet %ld; max detour %ld steps; max cells touched %d; detour lengths <10,<80,<640,<5120,...: %ld %ld %ld %ld %ld %ld %ld %ld\n",
   uses,ok+bad,ok,bad,maxk,maxspan,hist[0],hist[1],hist[2],hist[3],hist[4],hist[5],hist[6],hist[7]);
}
