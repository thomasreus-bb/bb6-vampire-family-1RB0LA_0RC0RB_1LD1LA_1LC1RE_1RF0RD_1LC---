/* nxt: run a 6-state TM from a given tape until the next macro configuration.
   usage: nxt TM pre x y startform maxsteps
   tape = pre (10)^x 1^y  (pre = "" or "1"); startform A: head left of tape, state A;
   startform B: tape pre (10)^x 1, head right of it, state B (y ignored).
   Stops at the first record event (new leftmost / rightmost head position) with
     A-form: state A, head left of all 1s, tape = pre (10)^X 1^Y   -> prints "A X Y steps"
     Bell:   state B, head = rightmost 1 + 1, tape = pre (10)^N 1   -> prints "B N steps"
   or HALT / MAX. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 4000000
static unsigned char t[W];
int T[6][2][3];
int main(int argc,char**argv){
  const char*M=argv[1]; const char*pre=argv[2]; long x=atol(argv[3]), y=atol(argv[4]); char sf=argv[5][0]; long long mx=atoll(argv[6]);
  for(int s=0;s<6;s++)for(int b=0;b<2;b++){const char*p=M+7*s+3*b; if(p[2]=='-'){T[s][b][2]=-1;continue;} T[s][b][0]=p[0]-'0';T[s][b][1]=p[1]=='R'?1:-1;T[s][b][2]=p[2]-'A';}
  long base=W/2, h, lo, hi; long pl=strlen(pre);
  long p=base; for(long i=0;i<pl;i++) t[p++]=pre[i]-'0'; for(long i=0;i<x;i++){t[p++]=1;t[p++]=0;}
  if(sf=='A'){ for(long i=0;i<y;i++) t[p++]=1; h=base-1; } else { t[p++]=1; h=p; }
  int s= sf=='A'?0:1; lo=base<h?base:h; hi=(p-1)>h?(p-1):h; long long n=0;
  while(n<mx){
    int b=t[h]; if(T[s][b][2]<0){printf("HALT %lld\n",n);return 0;}
    t[h]=T[s][b][0]; h+=T[s][b][1]; s=T[s][b][2]; n++;
    int rec=0; if(h<lo){lo=h;rec=1;} if(h>hi){hi=h;rec=2;}
    if(h<=1||h>=W-2){printf("TAPE %lld\n",n);return 0;}
    if(rec){
      long a=lo; while(a<=hi&&!t[a])a++; long z=hi; while(z>=a&&!t[z])z--;
      if(z<a) continue;
      if(s==0 && rec==1 && h<a){ long q=a; int ok=1; for(long i=0;i<pl;i++,q++) if(t[q]!=pre[i]-'0') ok=0;
        if(ok){ long X=0; while(q+1<=z && t[q]==1&&t[q+1]==0){X++;q+=2;} long Y=0; while(q<=z&&t[q]==1){Y++;q++;}
          if(q==z+1 && X>0){printf("A %ld %ld %lld\n",X,Y,n);return 0;} } }
      if(s==1 && rec==2 && h==z+1){ long q=a; int ok=1; for(long i=0;i<pl;i++,q++) if(t[q]!=pre[i]-'0') ok=0;
        if(ok){ long X=0; while(q+1<=z && t[q]==1&&t[q+1]==0){X++;q+=2;} if(q==z && t[q]==1){printf("B %ld %lld\n",X,n);return 0;} } }
    }
  }
  printf("MAX %lld\n",n); return 0;
}
