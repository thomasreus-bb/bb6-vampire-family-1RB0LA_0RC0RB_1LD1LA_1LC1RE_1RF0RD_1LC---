// iterate the exact band map of 1RB---_0RC0RD_1LD1RB_0LE0LC_1RA0LF_1LD1LE
#include <stdio.h>
#include <stdlib.h>
typedef long long ll;
static const int TAB[3][2][2][5]={ // [b%3][e][sep] -> d,bead,da,e2,dy
 {{{-1,1,3,1,0},{-1,0,3,1,-1}},{{0,0,1,0,0},{-1,1,4,1,-1}}},
 {{{0,0,2,0,0},{0,0,2,0,-1}},{{0,1,3,0,0},{0,0,3,0,-1}}},
 {{{0,0,1,1,0},{-1,1,4,0,-1}},{{0,0,2,1,0},{0,0,2,1,-1}}}};
int main(int c,char**v){ ll N=atoll(v[1]); ll a=1,b=1; int sep=1,e=1; ll cnt[4]={0}; ll every=c>2?atoll(v[2]):0; ll minY=1LL<<62,minYk=0;
 for(ll k=1;k<=N;k++){
   char lab;
   if(b==0){ lab='Z';
     if(sep==0&&e==0){ printf("HALT at the start of band %lld: a=%lld\n",k,a); return 0; }
     if(sep==0){ b=a; a=1; sep=1; e=0; } else if(e==0){ b=a+1; a=1; e=1; } else { b=a+1; a=2; e=1; }
     cnt[3]++; continue; }
   const int*t=TAB[b%3][e][sep]; ll m=2*b/3+t[0]; ll L=2*a+1+2*sep;
   if(L>m){ lab=(a<=b)?'A':'B'; cnt[lab-'A']++; ll a2=2*m+t[2]; ll Y2=2*a+3*sep-m+t[4]; a=a2; sep=1; e=t[3]; b=(Y2-e)/2; }
   else { cnt[2]++; ll Y=2*b+e-3*L-2-sep; ll a2=2*L+2+sep;
     if(Y<=0){ printf("HALT in band %lld (C band leaves right register %lld): a'=%lld\n",k+1,Y,a2); printf("A %lld B %lld C %lld Z %lld\n",cnt[0],cnt[1],cnt[2],cnt[3]); return 0; }
     if(Y<minY){minY=Y;minYk=k;}
     a=a2; sep=0; b=Y/2; e=Y%2; }
   if(every&&k%every==0){ printf("band %lld: a=%lld b=%lld  A %lld B %lld C %lld Z %lld\n",k,a,b,cnt[0],cnt[1],cnt[2],cnt[3]); fflush(stdout);} }
 printf("no halt in %lld bands; a=%lld b=%lld; A %lld B %lld C %lld Z %lld\n",N,a,b,cnt[0],cnt[1],cnt[2],cnt[3]); }
