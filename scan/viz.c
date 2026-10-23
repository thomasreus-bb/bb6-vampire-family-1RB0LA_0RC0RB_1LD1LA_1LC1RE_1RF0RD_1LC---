// viz: space-time diagram of a TM (bbchallenge notation, any states/symbols) from the blank tape,
// up to the start of Bell NB+1 (Bell starts = records of the longest block w^c, |w|<=3, with > 20 % growth,
// detected at new tape extremes).  Writes a binary PPM: one row per sampled step (at most H rows),
// one pixel column per cell (scaled up to at least MINW pixels); nonzero symbols orange, 0 white.
// usage: viz TM out.ppm NB H maxsteps
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int W[16][16],D[16][16],N[16][16],ns,nsym;
static void parse(const char*M){ ns=1; for(const char*p=M;*p;p++) if(*p=='_') ns++; nsym=(int)(strchr(M,'_')-M)/3;
  for(int i=0;i<ns;i++)for(int b=0;b<nsym;b++){const char*x=M+(3*nsym+1)*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';} }
static long longest(unsigned char*t,long a,long z){ long best=0; long x=a;
  while(x<=z){ long bc=1; int bp=1; for(int q=1;q<=3;q++){ long c=1; while(x+(c+1)*q-1<=z && !memcmp(t+x,t+x+c*q,q)) c++; if(c>=4&&c*q>bc*bp){bc=c;bp=q;} }
    int nz=0; for(int i=0;i<bp;i++) nz|=t[x+i]; if(bc>=4&&nz&&bc>best) best=bc; x+= bc>=4? bc*bp:1; } return best; }
int main(int argc,char**argv){
  const char*M=argv[1]; const char*out=argv[2]; int NB=atoi(argv[3]); int H=atoi(argv[4]); long long maxs=atoll(argv[5]); long maxspan=argc>6?atol(argv[6]):1000000;
  parse(M); long L=1<<22; unsigned char*t=calloc(L,1); long h=L/2,lo=h,hi=h; int s=0; long long n; int lev=0; long rec=0; int halted=0;
  for(n=0;n<maxs;n++){ int b=t[h]; if(N[s][b]<0){halted=1;break;} t[h]=W[s][b]; h+=D[s][b]; s=N[s][b];
    int ev=0; if(h<lo){lo=h;ev=1;} if(h>hi){hi=h;ev=1;}
    if(h<1||h>=L-1) break;
    if(hi-lo+1>maxspan) break;
    if(ev && hi-lo<200000){ long c=longest(t,lo,hi); if(c>=4 && c>rec*1.2){ lev++; rec=c; if(lev>NB) break; } else if(c>rec) rec=c; } }
  long long steps=n; long lo1=lo,hi1=hi;
  // pass 2
  memset(t,0,L); h=L/2; s=0; long span=hi1-lo1+1; int sc=1; while(span*sc<300) sc++;
  int rows= steps<H? (int)steps+1 : H; FILE*f=fopen(out,"wb"); fprintf(f,"P6\n%ld %d\n255\n",span*sc,rows);
  unsigned char*row=malloc(span*sc*3); int r=0;
  for(n=0;n<=steps && r<rows;n++){
    if((long long)r*steps/(rows>1?rows-1:1) <= n){ // emit row r at step n
      for(long x=0;x<span;x++){ int v=t[lo1+x]; unsigned char R=255,G=255,B=255; if(v){ R=255; G=165-(v-1)*25; B=0; } if(lo1+x==h){R=60;G=60;B=60;}
        for(int k=0;k<sc;k++){ long p=(x*sc+k)*3; row[p]=R; row[p+1]=G; row[p+2]=B; } }
      fwrite(row,1,span*sc*3,f); r++; }
    if(n==steps) break;
    int b=t[h]; if(N[s][b]<0) break; t[h]=W[s][b]; h+=D[s][b]; s=N[s][b]; }
  while(r<rows){ fwrite(row,1,span*sc*3,f); r++; }
  fclose(f);
  printf("%s steps=%lld levels=%d span=%ld halted=%d\n",M,steps,lev>NB?NB:lev,span,halted);
}
