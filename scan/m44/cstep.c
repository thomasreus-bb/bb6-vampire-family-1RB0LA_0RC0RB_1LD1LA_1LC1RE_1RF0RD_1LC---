/* cstep: macro step of no. 51 (and its table) on C(m, r) = [0] 10 1^m r, state A, head on the blank
   left of the tape; r = "" or a word starting with 0 (its trailing zeros are dropped).
   usage: cstep TM m r maxsteps   ->  prints "C m' r' steps" | "HALT steps" | "MAX steps"
   The next C configuration is the next left record in state A whose tape is 10 1^k w with k >= KMIN
   and w = "" or starting with 0, |w| <= 64. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 8000000
static unsigned char t[W]; int T[6][2][3];
int main(int argc,char**argv){
  const char*M=argv[1]; long m=atol(argv[2]); const char*r=argv[3]; long long mx=atoll(argv[4]); long KMIN=argc>5?atol(argv[5]):4;
  if(!strcmp(r,"-")) r="";
  for(int s=0;s<6;s++)for(int b=0;b<2;b++){const char*p=M+7*s+3*b; if(p[2]=='-'){T[s][b][2]=-1;continue;} T[s][b][0]=p[0]-'0';T[s][b][1]=p[1]=='R'?1:-1;T[s][b][2]=p[2]-'A';}
  long base=W/4,p=base; t[p++]=1;t[p++]=0; for(long i=0;i<m;i++) t[p++]=1; for(size_t i=0;i<strlen(r);i++) t[p++]=r[i]-'0';
  long h=base-1, lo=h, hi=p; int s=0; long long n=0;
  while(n<mx){ int b=t[h]; if(T[s][b][2]<0){printf("HALT %lld\n",n);return 0;}
    t[h]=T[s][b][0]; h+=T[s][b][1]; s=T[s][b][2]; n++;
    if(h<=0||h>=W-1){printf("TAPE %lld\n",n);return 0;}
    if(h<lo){ lo=h; if(s==0){ long a=h+1; while(a<=hi&&!t[a])a++; long z=hi; while(z>=a&&!t[z])z--;
        if(a<=z-1 && t[a]==1&&t[a+1]==0){ long q=a+2,k=0; while(q<=z&&t[q]==1){k++;q++;}
          if(k>=KMIN && (q>z || (t[q]==0 && z-q+1<=64))){ printf("C %ld ",k); for(long i=q;i<=z;i++) putchar('0'+t[i]); printf(" %lld\n",n); return 0; } } } }
    if(h>hi) hi=h; }
  printf("MAX %lld\n",n); return 0; }
