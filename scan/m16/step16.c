/* no. 16: one macro step.  start: P 1^a (01)^b, head on the 0 right of it, state C,
   where P = empty (m<0) or P = 1(10)^m.  Runs to the next new rightmost position in state C
   whose tape is P' 1^a' (01)^b' with a',b' >= 1 and P' empty or 1(10)^m'.
   usage: step16 m a b [limit]   prints: steps m' a' b'   (or HALT steps / MAX) */
#include <stdio.h>
#include <stdlib.h>
#define N (1<<25)
static unsigned char t[N];
int main(int argc,char**argv){
  long m=atol(argv[1]),a=atol(argv[2]),b=atol(argv[3]);
  long long lim=argc>4?atoll(argv[4]):4000000000LL;
  int wr[6][2]={{1,1},{1,1},{0,1},{0,1},{0,1},{1,0}};
  int mv[6][2]={{1,-1},{1,1},{-1,1},{0,-1},{1,1},{-1,-1}};
  int ns[6][2]={{1,5},{2,5},{3,4},{-1,2},{1,4},{0,4}};
  long h=N/4;
  if(m>=0){t[h++]=1; for(long i=0;i<m;i++){t[h++]=1;t[h++]=0;}}
  for(long i=0;i<a;i++)t[h++]=1;
  for(long i=0;i<b;i++){t[h++]=0;t[h++]=1;}
  long hi=h; int s=2; long long n=0;
  while(n<lim){
    int c=t[h]; int q=ns[s][c];
    if(q<0){printf("HALT %lld\n",n);return 0;}
    t[h]=wr[s][c]; h+=mv[s][c]; s=q; n++;
    if(h<8||h>N-8){printf("EDGE\n");return 1;}
    if(h>hi){hi=h; if(s==2&&t[h]==0){
      long p=h-1,bb=0; while(t[p]==1&&t[p-1]==0){bb++;p-=2;}
      long aa=0; while(t[p]==1){aa++;p--;}
      /* aa may have swallowed the leading 1 of P: P = 1(10)^m ends with 0 so fine; but
         P=1 (m=0) merges: treat as ambiguity -> report raw */
      if(aa<1||bb<1)continue;
      /* prefix: everything left of p */
      long z=p; int ok=1; long mm=0;
      /* expect (10)^mm then 1 then zeros, reading leftwards: t[z]=0,t[z-1]=1 ... */
      while(t[z]==0&&t[z-1]==1&&!(t[z-2]==0&&t[z-3]==0&&t[z-1]==1&&0)){ if(t[z-2]==0&&t[z-3]==0)break; mm++; z-=2;}
      long rest=0; for(long k=8;k<=z;k++)if(t[k]){rest=1;break;}
      if(!rest){printf("%lld -1 %ld %ld\n",n,aa,bb);return 0;}
      if(t[z]==1){ int clean=1; for(long k=8;k<z;k++)if(t[k]){clean=0;break;}
        if(clean){printf("%lld %ld %ld %ld\n",n,mm,aa,bb);return 0;} }
      /* other prefix: keep going */
    }}
  }
  printf("MAX\n"); return 0;
}
