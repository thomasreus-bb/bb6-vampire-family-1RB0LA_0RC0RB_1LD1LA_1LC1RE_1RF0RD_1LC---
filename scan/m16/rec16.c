/* no. 16 = 1RB1LF_1RC1RF_0LD1RE_---1LC_0RB1RE_1LA0LE : naive simulation from blank tape.
   At every new rightmost head position in state C, parse the tape right-to-left as
   P (1)^a (01)^b [head on 0] and print step, a, b and an RLE of the prefix P (abbreviated). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N (1<<24)
static unsigned char t[N];
int main(int argc,char**argv){
  long long lim=atoll(argv[1]);
  int wr[6][2]={{1,1},{1,1},{0,1},{0,1},{0,1},{1,0}};
  int mv[6][2]={{1,-1},{1,1},{-1,1},{0,-1},{1,1},{-1,-1}};
  int ns[6][2]={{1,5},{2,5},{3,4},{-1,2},{1,4},{0,4}};
  long h=N/2,hi=h,lo=h; int s=0; long long n=0;
  while(n<lim){
    int c=t[h]; int q=ns[s][c];
    if(q<0){printf("HALT at step %lld\n",n);return 0;}
    t[h]=wr[s][c]; h+=mv[s][c]; s=q; n++;
    if(h<lo)lo=h;
    if(h>hi){hi=h; if(s==2){
      long p=h-1; int b=0; while(t[p]==1&&t[p-1]==0&&!(t[p-2]==1&&0)){ /* (01) pairs */
        if(t[p]==1&&t[p-1]==0){b++;p-=2;} else break;}
      /* undo greedy: the block 1^a must be >=1, pairs end where a 11 appears */
      int a=0; long q2=p; while(t[q2]==1){a++;q2--;}
      if(a==0 && b>0){ /* last pair's 0 belongs before? keep */ }
      printf("%lld a=%d b=%d |",n,a,b);
      /* RLE of prefix lo..q2 */
      long k=lo; int cnt=0;
      while(k<=q2 && cnt<40){int v=t[k];long r=0;while(k<=q2&&t[k]==v){r++;k++;} printf(" %d^%ld",v,r);cnt++;}
      if(k<=q2)printf(" ...");
      printf("\n");
    }}
  }
  printf("END %lld\n",n);
}
