// mb K GROW < lines "h b1 ... bk": iterate macro steps (clean tape, state A on a 0) of no. 31 from each start,
// at most K macro steps or until the tape has grown by the factor GROW/100; prints "HALT j" (j = macro steps done) or "OK j h | blocks" or "TIMEOUT j"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char*M="1RB1RF_1RC0LD_1LB1RA_1RE1LE_0RC0LB_0RB---";
int W[6][2],D[6][2],N[6][2];
static unsigned char*tp; static long lo,hi,zz;
static inline int pz(long k){ return k>=lo&&k+1<=hi&&tp[k]==0&&tp[k+1]==0; }
int main(int c,char**v){ int K=atoi(v[1]); long GROW=atol(v[2]); long long MX=c>3?atoll(v[3]):2000000000LL;
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 static char line[1<<16]; long SZ=1<<24; tp=calloc(SZ,1);
 while(fgets(line,sizeof line,stdin)){ char*s=line; int h=strtol(s,&s,10); long bl[256]; int k=0; for(;;){char*e; long a=strtol(s,&e,10); if(e==s)break; s=e; bl[k++]=a;}
  long base=SZ/2, pos=base, head=-1, tot=0; if(h==0) head=base-1;
  for(int i=0;i<k;i++){ for(long j=0;j<bl[i];j++) tp[pos++]=1; if(i==h-1) head=pos; pos++; tot+=bl[i]+1; }
  lo=base-1; hi=pos; if(head<lo) lo=head; if(head>hi) hi=head; zz=0; for(long j=lo;j<hi;j++) zz+=pz(j);
  long p=head; int q=0; long long st=0; int j=0; int res=0; long mlo=lo,mhi=hi; long a=0,e=0; int hh=0;
  while(1){ int b=tp[p];
   if(st>0&&q==0&&b==0){ a=lo; while(a<=hi&&tp[a]==0) a++; e=hi; while(e>=a&&tp[e]==0) e--;
     long lead= a-lo>=2? a-lo-1:0; long trail= hi-e>=2? hi-e-1:0;
     if(a<=e && zz-lead-trail==0 && p>=a-1 && p<=e+1){ j++; hh=0; for(long x=a;x<p;x++) if(tp[x]==0) hh++; if(p>=a) hh++; if(p==a-1) hh=0;
        if(j>=K || (e-a+1)*100>tot*GROW){ res=1; break; } } }
   if(N[q][b]<0){ res=2; break; }
   int w=W[q][b]; if(w!=b){ zz-=pz(p-1)+pz(p); tp[p]=w; zz+=pz(p-1)+pz(p); }
   p+=D[q][b]; q=N[q][b]; st++;
   if(st>MX){ res=3; break; }
   if(p<2||p>=SZ-2){ res=4; break; }
   if(p<lo){ lo=p; zz+=pz(lo); if(lo<mlo)mlo=lo; } if(p>hi){ hi=p; zz+=pz(hi-1); if(hi>mhi)mhi=hi; } }
  if(res==2) printf("HALT %d\n",j); else if(res==3) printf("TIMEOUT %d\n",j); else if(res==4) printf("EDGE %d\n",j);
  else { printf("OK %d %d |",j,hh); long cur=0; for(long x=a;x<=e;x++){ if(tp[x]) cur++; else { printf(" %ld",cur); cur=0; } } printf(" %ld\n",cur); }
  memset(tp+mlo-2,0,mhi-mlo+5); }
 return 0; }
