/* trace: run a TM from tape = pre (10)^x 1^y (start A: head left, state A) and print every
   record event (new leftmost / rightmost position) with state and RLE tape. usage: trace TM pre x y maxsteps */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 4000000
static unsigned char t[W]; int T[6][2][3];
static void rle(long a,long z,long h){ /* runs of period 1 or 2 */
  long i=a; while(i<=z){ if(i==h) printf("["); 
    long c=1; if(i+1<=z){ int p0=t[i],p1=t[i+1]; long j=i; while(j+1<=z&&t[j]==p0&&t[j+1]==p1&&!(h>=j&&h<=j+1&&j!=i)) {j+=2;} long k2=(j-i)/2;
      if(k2>=3 && !(p0==p1)){ printf("(%d%d)^%ld ",p0,p1,k2); i+=2*k2; continue; } }
    long j=i; while(j<=z&&t[j]==t[i]&&(j==i||j!=h)) j++; c=j-i;
    if(c>=3){ printf("(%d)^%ld ",t[i],c); i=j; continue; }
    printf("%d%s",t[i], i==h?"] ":""); i++; }
  printf("\n"); }
int main(int argc,char**argv){
  const char*M=argv[1]; const char*pre=argv[2]; long x=atol(argv[3]), y=atol(argv[4]); long long mx=atoll(argv[5]);
  for(int s=0;s<6;s++)for(int b=0;b<2;b++){const char*p=M+7*s+3*b; if(p[2]=='-'){T[s][b][2]=-1;continue;} T[s][b][0]=p[0]-'0';T[s][b][1]=p[1]=='R'?1:-1;T[s][b][2]=p[2]-'A';}
  long base=W/2,p=base; long pl=strlen(pre); for(long i=0;i<pl;i++) t[p++]=pre[i]-'0'; for(long i=0;i<x;i++){t[p++]=1;t[p++]=0;} for(long i=0;i<y;i++) t[p++]=1;
  long h=base-1, lo=h, hi=p-1; int s=0; long long n=0;
  while(n<mx){ int b=t[h]; if(T[s][b][2]<0){printf("HALT %lld\n",n);return 0;}
    t[h]=T[s][b][0]; h+=T[s][b][1]; s=T[s][b][2]; n++;
    int rec=0; if(h<lo){lo=h;rec=1;} if(h>hi){hi=h;rec=2;}
    if(rec){ long a=lo; while(a<=hi&&!t[a])a++; long z=hi; while(z>=a&&!t[z])z--; printf("%c %lld st%c: ",rec==1?'L':'R',n,'A'+s); rle(a<h?a:h,z>h?z:h,h);} }
  return 0; }
