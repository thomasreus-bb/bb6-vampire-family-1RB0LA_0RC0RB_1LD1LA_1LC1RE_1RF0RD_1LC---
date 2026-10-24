// bstep: run a TM from the Bell configuration  L w^n T  (head at the right end if side R, left end if L, given state)
// to the next event of the same side and state where the tape (between the extremes) reads L' w^c T' with
// c >= thr*n, |L'| <= maxl, |T'| <= maxl (w^c = the longest run of w).  Prints "OK L' c T' steps" | "HALT steps" | "FAIL".
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc,char**argv){
  const char*M=argv[1]; int side=argv[2][0]; int st0=argv[3][0]-'A'; const char*w=argv[4];
  const char*Ls=strcmp(argv[5],"-")?argv[5]:""; const char*Ts=strcmp(argv[6],"-")?argv[6]:"";
  long long n=atoll(argv[7]); double thr=atof(argv[8]); int maxl=atoi(argv[9]); long long maxs=atoll(argv[10]);
  int ns=1; for(const char*q=M;*q;q++) if(*q=='_') ns++; int nsym=(int)(strchr(M,'_')-M)/3;
  int W[16][16],D[16][16],N[16][16];
  for(int i=0;i<ns;i++)for(int b=0;b<nsym;b++){const char*x=M+(3*nsym+1)*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
  int wl=strlen(w); long long len=strlen(Ls)+wl*n+strlen(Ts); long long L=6*len+(1<<20);
  unsigned char*t=calloc(L,1); long long lo=L/2,x=lo;
  for(const char*p=Ls;*p;p++) t[x++]=*p-'0'; for(long long k=0;k<n;k++) for(int i=0;i<wl;i++) t[x++]=w[i]-'0'; for(const char*p=Ts;*p;p++) t[x++]=*p-'0';
  long long hi=x-1, h= side=='R'?hi:lo; int s=st0;
  for(long long step=0;step<maxs;step++){
    int b=t[h]; if(N[s][b]<0){ printf("HALT %lld\n",step); return 0; }
    t[h]=W[s][b]; h+=D[s][b]; s=N[s][b];
    if(h<1||h>=L-1){ printf("FAIL\n"); return 0; }
    int ev=0; if(h<lo){lo=h;ev='L';} else if(h>hi){hi=h;ev='R';}
    if(ev!=side||s!=st0) continue;
    if(hi-lo+1 < (long long)(thr*n)*wl) continue;
    // longest run of w (any alignment)
    long long bestc=0,bests=0;
    for(int off=0;off<wl;off++){ long long c=0,cs=0; for(long long y=lo+off;y+wl-1<=hi;y+=wl){ int m=1; for(int i=0;i<wl;i++) if(t[y+i]!=w[i]-'0'){m=0;break;} if(m){ if(!c) cs=y; c++; if(c>bestc){bestc=c;bests=cs;} } else c=0; } }
    if(bestc<(long long)(thr*n)) continue;
    long long ll=bests-lo, tl=hi-(bests+bestc*wl)+1;
    if(ll>maxl||tl>maxl) continue;
    printf("OK ");
    if(ll==0) printf("-"); for(long long y=lo;y<bests;y++) putchar('0'+t[y]);
    printf(" %lld ",bestc);
    if(tl==0) printf("-"); for(long long y=bests+bestc*wl;y<=hi;y++) putchar('0'+t[y]);
    printf(" %lld\n",step); return 0; }
  printf("FAIL\n"); return 0; }
