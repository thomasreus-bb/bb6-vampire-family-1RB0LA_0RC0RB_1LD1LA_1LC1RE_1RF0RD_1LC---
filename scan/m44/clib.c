/* library version of cstep for ctypes (see cstep.c): returns 1 = C reached, 2 = HALT, 0 = MAX/TAPE */
#include <string.h>
#define W 4000000
static unsigned char t[W]; static int T[6][2][3]; static int inited=0;
void setup(const char*M){ for(int s=0;s<6;s++)for(int b=0;b<2;b++){const char*p=M+7*s+3*b; if(p[2]=='-'){T[s][b][2]=-1;continue;} T[s][b][0]=p[0]-'0';T[s][b][1]=p[1]=='R'?1:-1;T[s][b][2]=p[2]-'A';} inited=1; }
int cstep(long m, const char*r, long long mx, long kmin, long*mout, char*rout, long long*steps){
  long base=W/4,p=base; memset(t,0,W); t[p++]=1;t[p++]=0; for(long i=0;i<m;i++) t[p++]=1; for(size_t i=0;i<strlen(r);i++) t[p++]=r[i]-'0';
  long h=base-1, lo=h, hi=p; int s=0; long long n=0;
  while(n<mx){ int b=t[h]; if(T[s][b][2]<0){*steps=n; return 2;}
    t[h]=T[s][b][0]; h+=T[s][b][1]; s=T[s][b][2]; n++;
    if(h<=0||h>=W-1) return 0;
    if(h<lo){ lo=h; if(s==0){ long a=h+1; while(a<=hi&&!t[a])a++; long z=hi; while(z>=a&&!t[z])z--;
        if(a<=z-1 && t[a]==1&&t[a+1]==0){ long q=a+2,k=0; while(q<=z&&t[q]==1){k++;q++;}
          if(k>=kmin && (q>z || (t[q]==0 && z-q+1<=200))){ *mout=k; long j=0; for(long i=q;i<=z;i++) rout[j++]='0'+t[i]; rout[j]=0; *steps=n; return 1; } } } }
    if(h>hi) hi=h; }
  *steps=n; return 0; }
