// level.c -- level Q1 Q2 < lines "r w1 w2 ...": one level of M (mirrored A) from  (110)^(2q+r) W, state D, head left of the tape,
// for q = Q1 and q = Q2, until the next D-configuration that starts with at least two runs of 2.
// prints "e w1' w2' ..." (n' = 3q + e, both q must agree, else DIFF), or HALT / MAX / EDGE.  W must not start with a run of 2.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
const char*M="1LB1RF_1RC1LD_1LA1RA_0LA0LE_0LC---_1LF0RC";
int Wr[8][2],D[8][2],N[8][2];
#define SZ (1L<<25)
static unsigned char t[SZ];
static long res[2][1<<20]; long rl[2];
int one(long n,long*w,long nw,long*out,long*nout,long long maxs){
  long base=SZ/8; long p=base,x=base+1,lo=p,hi;
  for(long i=0;i<n;i++){t[x]=1;t[x+1]=1;x+=3;}
  for(long i=0;i<nw;i++){ for(long j=0;j<w[i];j++)t[x++]=1; x++; }
  hi=x; long first=base+1; int q=3; int ret=2;
  for(long long st=0;st<maxs;st++){ int b=t[p]; if(N[q][b]<0){ret=1;break;} t[p]=Wr[q][b]; if(Wr[q][b]&&p<first)first=p;
   p+=D[q][b]; q=N[q][b]; if(p<lo)lo=p; if(p>hi)hi=p; if(p<=1||p>=SZ-2){ret=3;break;}
   if(q==3&&p<first){ while(first<=hi&&!t[first])first++;
    if(p==first-1 && t[first+1]&&!t[first+2]&&t[first+3]&&t[first+4]&&!t[first+5]){ long h=hi; while(h>p&&!t[h])h--;
       long i=first,k=0; while(t[i]&&t[i+1]&&!t[i+2]&&i+2<=h+1){k++;i+=3;}
       out[0]=k; long c=1,run=0; for(;i<=h+1;i++){ if(t[i])run++; else {out[c++]=run;run=0;} } *nout=c; ret=0; break; } } }
  memset(t+lo-1,0,hi-lo+3); return ret; }
int main(int c,char**v){ long Q[2]={atol(v[1]),atol(v[2])}; long long maxs=c>3?atoll(v[3]):20000000000LL;
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} Wr[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 static char line[1<<22]; static long w[1<<20];
 while(fgets(line,sizeof line,stdin)){ char*s=line; long r=strtol(s,&s,10); long nw=0; for(;;){char*e; long a=strtol(s,&e,10); if(e==s)break; s=e; w[nw++]=a;}
  int bad=0; for(int k=0;k<2;k++){ int rc=one(2*Q[k]+r,w,nw,res[k],&rl[k],maxs); if(rc){ printf(rc==1?"HALT\n":rc==2?"MAX\n":"EDGE\n"); bad=1; break; } res[k][0]-=3*Q[k]; }
  if(bad) {fflush(stdout);continue;}
  if(rl[0]!=rl[1]||memcmp(res[0],res[1],rl[0]*sizeof(long))){ printf("DIFF\n"); fflush(stdout); continue; }
  for(long i=0;i<rl[0];i++) printf(i?" %ld":"%ld",res[0][i]); printf("\n"); fflush(stdout); }
}
