// bmap2: iterate the exact Bell map of 1RB---_0RC0RD_1LD1RB_0LE0LC_1RA0LF_1LD1LE with exact step count.
// usage: bmap2 NBELLS [REPORT_EVERY [a sep b e START_STEPS]]
// A Bell starts when the head enters a new cell at the left end in state C; the tape is then
//   0 (01)^a [0 01 if sep] (11)^b [1 if e], head on the leftmost 0.  Bell 1 starts at step 48 with a=1,sep=1,b=1,e=1.
// Steps per Bell (exact, fitted on 44,000 single-Bell runs of the real TM and checked against the orbit):
//   C Bell:   16a^2+38a+21 (sep=0),  16a^2+78a+91 (sep=1)
//   A/B Bell (also b=0): (96ab - 16b^2 + k1 a + k2 b + k0)/9 with k from table KS[b%3][e][sep]
// HALT: start tape 0 (01)^x [0] with nothing else -> 16+6x steps, then the halting transition.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll; typedef __int128 i128; typedef unsigned __int128 u128;
static const int TAB[3][2][2][5]={ // [b%3][e][sep] -> d,bead,da,e2,dy
 {{{-1,1,3,1,0},{-1,0,3,1,-1}},{{0,0,1,0,0},{-1,1,4,1,-1}}},
 {{{0,0,2,0,0},{0,0,2,0,-1}},{{0,1,3,0,0},{0,0,3,0,-1}}},
 {{{0,0,1,1,0},{-1,1,4,0,-1}},{{0,0,2,1,0},{0,0,2,1,-1}}}};
static const int KS[3][2][2][3]={ // k0,k1,k2
 {{{207,198,48},{387,198,168}},{{153,198,48},{549,270,144}}},
 {{{149,174,56},{335,174,176}},{{227,246,32},{467,246,152}}},
 {{{125,150,64},{473,222,160}},{{173,222,40},{419,222,160}}}};
// 192-bit unsigned accumulator
typedef struct { u128 lo; unsigned long long hi; } acc;
static void add(acc*A,u128 x){ u128 o=A->lo; A->lo+=x; if(A->lo<o) A->hi++; }
static void pr(acc A){ // decimal print
  unsigned int d[64]; int n=0; // base 1e9 limbs via repeated division of 192-bit number
  unsigned long long w[3]={(unsigned long long)A.lo,(unsigned long long)(A.lo>>64),A.hi}; char buf[80]; int bl=0;
  while(w[0]||w[1]||w[2]){ u128 r=0; for(int i=2;i>=0;i--){ u128 cur=(r<<64)|w[i]; w[i]=(unsigned long long)(cur/1000000000u); r=cur%1000000000u; } d[n++]=(unsigned)r; }
  if(!n){ printf("0"); return; } printf("%u",d[n-1]); for(int i=n-2;i>=0;i--) printf("%09u",d[i]); (void)buf;(void)bl; }
static double approx(acc A){ return (double)A.hi*18446744073709551616.0*18446744073709551616.0+(double)A.lo; }
int main(int c,char**v){ ll N=atoll(v[1]); ll every=c>2?atoll(v[2]):0; ll a=1,b=1; int sep=1,e=1; acc S={48,0};
 if(c>7){ a=atoll(v[3]); sep=atoi(v[4]); b=atoll(v[5]); e=atoi(v[6]); S.lo=(u128)atoll(v[7]); }
 ll cnt[4]={0};
 for(ll k=1;k<=N;k++){
   if(b==0&&sep==0&&e==0){ add(&S,(u128)(16+6*(i128)a)); printf("HALT in Bell %lld (start tape 0 (01)^%lld): steps ",k,a); pr(S); printf(" + 1 halting transition\n"); return 0; }
   const int*t=TAB[b%3][e][sep]; ll m=2*b/3+t[0]; ll L=2*a+1+2*sep;
   if(b==0 || L>m){ const int*K=KS[b%3][e][sep];
     i128 s9=(i128)96*a*b-(i128)16*b*b+(i128)K[1]*a+(i128)K[2]*b+K[0]; add(&S,(u128)(s9/9));
     if(b==0){ cnt[3]++; if(sep==0){ b=a; a=1; sep=1; e=0; } else if(e==0){ b=a+1; a=1; e=1; } else { b=a+1; a=2; e=1; } }
     else { cnt[a<=b?0:1]++; ll a2=2*m+t[2]; ll Y2=2*a+3*sep-m+t[4]; a=a2; sep=1; e=t[3]; b=(Y2-e)/2; } }
   else { cnt[2]++; i128 s=(i128)16*a*a+(sep?78:38)*(i128)a+(sep?91:21); add(&S,(u128)s);
     ll Y=2*b+e-3*L-2-sep; ll a2=2*L+2+sep;
     if(Y==-1){ add(&S,(u128)(16+6*(i128)(a2-1))); printf("HALT in Bell %lld (start tape 0 (01)^%lld 0): steps ",k+1,a2-1); pr(S); printf(" + 1 halting transition\n"); return 0; }
     if(Y<-1){ printf("unexpected remainder %lld in Bell %lld\n",Y,k); return 1; }
     a=a2; sep=0; b=Y/2; e=Y%2; }
   if(every&&k%every==0){ printf("Bell %lld done: a=%lld b=%lld steps %.6e  A %lld B %lld C %lld Z %lld\n",k,a,b,approx(S),cnt[0],cnt[1],cnt[2],cnt[3]); fflush(stdout);} }
 printf("no halt in %lld Bells; next a=%lld sep=%d b=%lld e=%d; steps ",N,a,sep,b,e); pr(S); printf("  A %lld B %lld C %lld Z %lld\n",cnt[0],cnt[1],cnt[2],cnt[3]); }
